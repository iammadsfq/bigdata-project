"""Benchmark: query speed CSV (raw) vs Iceberg (lakehouse).

Runs three representative analytical workloads against the same
lineitem data — once from raw CSV in MinIO, once from the
Iceberg/Parquet lakehouse — and reports runtimes side-by-side.

Each query is run once as a warm-up (not measured) before the timed
run, so JIT compilation and class loading don't skew the comparison.
"""

from __future__ import annotations

import os
import time

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from session import get_spark
from tpch_schemas import LINEITEM_SCHEMA

RAW_DATA_PATH = os.environ.get("RAW_DATA_PATH", "s3a://raw/tpch")
CSV_PATH = f"{RAW_DATA_PATH}/lineitem.csv"
ICEBERG_TABLE = "lakehouse.tpch.lineitem"


def time_action(df: DataFrame) -> float:
    """Force full execution of df and return wall-clock seconds.

    Uses count() since it forces a full scan but returns minimal data
    to the driver, so we measure execution not transfer.
    """
    start = time.perf_counter()
    df.count()
    return time.perf_counter() - start


def run_benchmark(label: str, csv_df: DataFrame, iceberg_df: DataFrame,
                  build_query):
    """Run the same logical query against CSV and Iceberg and print timing."""
    csv_q = build_query(csv_df)
    iceberg_q = build_query(iceberg_df)

    # warm-up
    csv_q.count()
    iceberg_q.count()

    csv_secs = time_action(csv_q)
    iceberg_secs = time_action(iceberg_q)

    speedup = csv_secs / iceberg_secs if iceberg_secs > 0 else float("inf")
    print(f"  {label:<35} CSV {csv_secs:>7.2f}s   Iceberg {iceberg_secs:>7.2f}s   speedup {speedup:>5.1f}x")


def main() -> int:
    spark = get_spark("Benchmark CSV vs Iceberg")
    spark.sparkContext.setLogLevel("WARN")

    csv_df = (
        spark.read
        .option("header", "false")
        .option("sep", "|")
        .schema(LINEITEM_SCHEMA)
        .csv(CSV_PATH)
    )
    iceberg_df = spark.table(ICEBERG_TABLE)

    print("\n=== Benchmark: CSV (raw) vs Iceberg (lakehouse) on lineitem ===\n")

    run_benchmark(
        "Q-full-scan: COUNT(*)",
        csv_df, iceberg_df,
        lambda df: df.select(F.lit(1).alias("dummy")),
    )

    run_benchmark(
        "Q-group-by: returnflag,linestatus",
        csv_df, iceberg_df,
        lambda df: df.groupBy("l_returnflag", "l_linestatus").count(),
    )

    run_benchmark(
        "Q-filter+sum: l_shipdate > 1997-01-01",
        csv_df, iceberg_df,
        lambda df: (
            df.filter(F.col("l_shipdate") > F.lit("1997-01-01"))
              .agg(F.sum("l_extendedprice").alias("revenue"))
        ),
    )

    print("\nNote: each query was run once as warm-up before timing.")
    print("Iceberg advantage comes from columnar Parquet + min/max stats")
    print("for predicate pushdown (no need to parse rows that don't match).")

    spark.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
