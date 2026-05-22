from __future__ import annotations

import os
import sys
import pyspark
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

    # Configure Spark with Iceberg and S3A packages (downloaded at init time)
    conf = (
        pyspark.SparkConf()
        .setAppName(f"Load {table}")
        .set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0')
        .set('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions')
        .set('spark.sql.defaultCatalog', 'lakehouse')
        .set('spark.sql.catalog.lakehouse', 'org.apache.iceberg.spark.SparkCatalog')
        .set('spark.sql.catalog.lakehouse.type', 'hadoop')
        .set('spark.sql.catalog.lakehouse.warehouse', 's3a://lakehouse/warehouse')
        .set('spark.hadoop.fs.s3a.endpoint', 'http://minio:9000')
        .set('spark.hadoop.fs.s3a.access.key', 'minio')
        .set('spark.hadoop.fs.s3a.secret.key', 'minio123')
        .set('spark.hadoop.fs.s3a.path.style.access', 'true')
        .set('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
    )

    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    spark.sql("CREATE DATABASE IF NOT EXISTS lakehouse.tpch")

    from tpch_schemas import SCHEMAS

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
