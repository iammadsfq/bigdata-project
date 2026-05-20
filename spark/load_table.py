from __future__ import annotations

import sys
from pyspark.sql import SparkSession


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: spark-submit load_table.py <table>")
        return 2

    table = sys.argv[1]
    # Prefer locally-generated CSVs if mounted into the container (faster, avoids S3A classpath issues)
    local_path = f"/data/tpch/{table}.csv"
    if os.path.exists(local_path):
        input_path = local_path
    else:
        input_path = f"s3a://raw/tpch/{table}.csv"
    target_table = f"lakehouse.tpch.{table}"

    spark = (
        SparkSession.builder
        .appName(f"Load {table}")
        .getOrCreate()
    )

    spark.sql("CREATE DATABASE IF NOT EXISTS lakehouse.tpch")

    df = (
        spark.read
        .option("header", "false")
        .option("inferSchema", "true")
        .option("sep", ",")
        .csv(input_path)
    )

    df.writeTo(target_table).createOrReplace()

    spark.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
