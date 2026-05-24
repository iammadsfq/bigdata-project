"""Benchmark: filter query speed on unpartitioned vs year-partitioned lineitem.

Creates a copy of lineitem partitioned by year(l_shipdate) (Iceberg
hidden partitioning), then runs the same filter+aggregation against
both tables to demonstrate partition pruning.

TPC-H lineitem.l_shipdate spans 1992-01-02 to 1998-12-01, so year
partitioning creates 7 partitions. A query filtering on a single
year should scan only 1/7 of the data.
"""

from __future__ import annotations

import time

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from session import get_spark


PARTITIONED_TABLE = "lakehouse.tpch.lineitem_partitioned"


def ensure_partitioned_table(spark) -> None:
    """Create lineitem_partitioned if it doesn't exist or is stale."""
    tables = [r.tableName for r in spark.sql("SHOW TABLES IN lakehouse.tpch").collect()]
    
    recreate = False
    if "lineitem_partitioned" in tables:
        print(f"  {PARTITIONED_TABLE} already exists. Checking for staleness...")
        unpartitioned_count = spark.table("lakehouse.tpch.lineitem").count()
        partitioned_count = spark.table(PARTITIONED_TABLE).count()
        if unpartitioned_count != partitioned_count:
            print(f"  WARNING: Row count mismatch (unpartitioned: {unpartitioned_count}, partitioned: {partitioned_count}). Table is stale!")
            print(f"  Dropping stale {PARTITIONED_TABLE}...")
            spark.sql(f"DROP TABLE IF EXISTS {PARTITIONED_TABLE}")
            recreate = True
        else:
            print(f"  {PARTITIONED_TABLE} is up-to-date (both have {unpartitioned_count} rows), skipping create.")
            return
    else:
        recreate = True

    if recreate:
        print(f"  Creating {PARTITIONED_TABLE} partitioned by years(l_shipdate)...")
        start = time.perf_counter()
        spark.sql(f"""
            CREATE TABLE {PARTITIONED_TABLE}
            USING iceberg
            PARTITIONED BY (years(l_shipdate))
            AS SELECT * FROM lakehouse.tpch.lineitem
        """)
        elapsed = time.perf_counter() - start
        print(f"  Done in {elapsed:.1f}s.")


def time_action(df: DataFrame) -> float:
    start = time.perf_counter()
    df.count()
    return time.perf_counter() - start


def main() -> int:
    spark = get_spark("Benchmark Partitioning")
    spark.sparkContext.setLogLevel("WARN")

    print("\n=== Setup ===")
    ensure_partitioned_table(spark)

    unpartitioned = spark.table("lakehouse.tpch.lineitem")
    partitioned   = spark.table(PARTITIONED_TABLE)

    print("\n=== Sanity: same row counts ===")
    unp_count = unpartitioned.count()
    par_count = partitioned.count()
    print(f"  unpartitioned: {unp_count:>10}")
    print(f"  partitioned:   {par_count:>10}")
    if unp_count != par_count:
        raise ValueError(
            f"Sanity check failed: Row count mismatch! Unpartitioned table has {unp_count} rows, "
            f"but partitioned table has {par_count} rows."
        )

    def build_filter_query(df: DataFrame):
        return (
            df.filter((F.col("l_shipdate") >= F.lit("1996-01-01")) &
                      (F.col("l_shipdate") <  F.lit("1997-01-01")))
              .agg(
                  F.sum("l_extendedprice").alias("revenue"),
                  F.count("*").alias("n_rows"),
              )
        )

    # warm-up
    build_filter_query(unpartitioned).count()
    build_filter_query(partitioned).count()

    print("\n=== Benchmark: filter to 1 year of data ===")
    unp_secs = time_action(build_filter_query(unpartitioned))
    par_secs = time_action(build_filter_query(partitioned))
    speedup = unp_secs / par_secs if par_secs > 0 else float("inf")

    print(f"  Unpartitioned  {unp_secs:>7.2f}s")
    print(f"  Partitioned    {par_secs:>7.2f}s")
    print(f"  Speedup        {speedup:>7.1f}x")

    print("\n=== Iceberg snapshot files scanned (1996 filter) ===")
    print("  Unpartitioned plan:")
    build_filter_query(unpartitioned).explain(mode="formatted")
    print("\n  Partitioned plan (look for partition filter pushdown):")
    build_filter_query(partitioned).explain(mode="formatted")

    spark.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
