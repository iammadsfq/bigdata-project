from __future__ import annotations

import pyspark
from pyspark.sql import SparkSession


def main() -> int:
    # Configure Spark with Iceberg and S3A packages (downloaded at init time)
    conf = (
        pyspark.SparkConf()
        .setAppName("Toy Query")
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

    from tpch_schemas import LINEITEM_SCHEMA

    csv_df = (
        spark.read
        .option("header", "false")
        .option("sep", "|")
        .schema(LINEITEM_SCHEMA)
        .csv("s3a://raw/tpch/lineitem.csv")
    )

    print("CSV group-by:")
    (
        csv_df.groupBy("l_shipdate")
        .count()
        .orderBy("l_shipdate")
        .show(20, truncate=False)
    )

    print("Iceberg group-by:")
    (
        spark.table("lakehouse.tpch.lineitem")
        .groupBy("l_shipdate")
        .count()
        .orderBy("l_shipdate")
        .show(20, truncate=False)
    )

    spark.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
