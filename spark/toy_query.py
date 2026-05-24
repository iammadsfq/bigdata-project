from __future__ import annotations

import os

from session import get_spark
from tpch_schemas import LINEITEM_SCHEMA


def main() -> int:
    spark = get_spark("Toy Query")

    raw_path = os.environ.get("RAW_DATA_PATH", "s3a://raw/tpch")
    csv_df = (
        spark.read
        .option("header", "false")
        .option("sep", "|")
        .schema(LINEITEM_SCHEMA)
        .csv(f"{raw_path}/lineitem.csv")
    )

    print("CSV group-by:")
    csv_df.groupBy("l_shipdate").count().orderBy("l_shipdate").show(20, truncate=False)

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
