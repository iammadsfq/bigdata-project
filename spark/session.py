from __future__ import annotations

import pyspark
from pyspark.sql import SparkSession


ICEBERG_PACKAGES = (
    "org.apache.hadoop:hadoop-aws:3.3.4,"
    "com.amazonaws:aws-java-sdk-bundle:1.12.262,"
    "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0"
)


def get_spark(app_name: str, extra_conf: dict[str, str] | None = None) -> SparkSession:
    conf = (
        pyspark.SparkConf()
        .setAppName(app_name)
        .set("spark.jars.packages", ICEBERG_PACKAGES)
        .set("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .set("spark.sql.defaultCatalog", "lakehouse")
        .set("spark.sql.catalog.lakehouse", "org.apache.iceberg.spark.SparkCatalog")
        .set("spark.sql.catalog.lakehouse.type", "hadoop")
        .set("spark.sql.catalog.lakehouse.warehouse", "s3a://lakehouse/warehouse")
        .set("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .set("spark.hadoop.fs.s3a.access.key", "minio")
        .set("spark.hadoop.fs.s3a.secret.key", "minio123")
        .set("spark.hadoop.fs.s3a.path.style.access", "true")
        .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    )
    for key, value in (extra_conf or {}).items():
        conf = conf.set(key, value)
    return SparkSession.builder.config(conf=conf).getOrCreate()
