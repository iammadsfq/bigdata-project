from __future__ import annotations

from pyspark.sql import SparkSession


def main() -> int:
    spark = SparkSession.builder.appName("Toy Query").getOrCreate()

    csv_df = (
        spark.read
        .option("header", "false")
        .option("inferSchema", "true")
        .option("sep", ",")
        .csv("s3a://raw/tpch/lineitem.csv")
    )

    print("CSV group-by:")
    (
        csv_df.groupBy("_c10")
        .count()
        .orderBy("_c10")
        .show(20, truncate=False)
    )

    print("Iceberg group-by:")
    (
        spark.table("lakehouse.tpch.lineitem")
        .groupBy("_c10")
        .count()
        .orderBy("_c10")
        .show(20, truncate=False)
    )

    spark.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
