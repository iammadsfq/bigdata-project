"""Initialize Iceberg schemas and load TPC-H CSV files from MinIO into Iceberg.

Usage:
  spark-submit /opt/spark/app/ingest/load_tables.py               # load all 8 TPC-H tables
  spark-submit /opt/spark/app/ingest/load_tables.py --init-only   # create schemas only
  spark-submit /opt/spark/app/ingest/load_tables.py orders lineitem  # load specific tables
"""

from __future__ import annotations

import os
import sys

from session import get_spark
from tpch_schemas import SCHEMAS

ALL_TABLES = list(SCHEMAS.keys())


def init_schemas(spark) -> None:
    """Ensure required Iceberg namespaces exist (default is required by Spark Thrift Server / dbt)."""
    for db in ("default", "tpch", "tpch_mart"):
        spark.sql(f"CREATE DATABASE IF NOT EXISTS lakehouse.{db}")


def main() -> int:
    args = sys.argv[1:]
    init_only = "--init-only" in args
    tables = [a for a in args if a != "--init-only"] or ALL_TABLES

    invalid = [t for t in tables if t not in SCHEMAS]
    if invalid:
        print(f"Unknown table(s): {', '.join(invalid)}. Valid: {', '.join(ALL_TABLES)}")
        return 2

    spark = get_spark("TPC-H Iceberg Loader")
    init_schemas(spark)

    if init_only:
        print("Initialized schemas: lakehouse.default, lakehouse.tpch, lakehouse.tpch_mart")
        spark.stop()
        return 0

    raw_path = os.environ.get("RAW_DATA_PATH", "s3a://raw/tpch")
    for table in tables:
        input_path = f"{raw_path}/{table}.csv"
        target_table = f"lakehouse.tpch.{table}"
        print(f"Loading {table} from {input_path} -> {target_table}...")
        df = (
            spark.read
            .option("header", "false")
            .option("sep", "|")
            .schema(SCHEMAS[table])
            .csv(input_path)
        )
        df.writeTo(target_table).createOrReplace()

    print("Iceberg load complete.")
    spark.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
