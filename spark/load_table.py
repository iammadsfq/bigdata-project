from __future__ import annotations

import os
import sys

from session import get_spark
from tpch_schemas import SCHEMAS


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: spark-submit load_table.py <table>")
        return 2

    table = sys.argv[1]
    raw_path = os.environ.get("RAW_DATA_PATH", "s3a://raw/tpch")
    input_path = f"{raw_path}/{table}.csv"
    target_table = f"lakehouse.tpch.{table}"

    spark = get_spark(f"Load {table}")
    spark.sql("CREATE DATABASE IF NOT EXISTS lakehouse.tpch")

    df = (
        spark.read
        .option("header", "false")
        .option("sep", "|")
        .schema(SCHEMAS[table])
        .csv(input_path)
    )

    df.writeTo(target_table).createOrReplace()
    spark.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
