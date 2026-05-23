from __future__ import annotations

from session import get_spark


EXPECTED_ROWS_SF1 = {
    "region":   5,
    "nation":   25,
    "supplier": 10_000,
    "customer": 150_000,
    "part":     200_000,
    "partsupp": 800_000,
    "orders":   1_500_000,
    "lineitem": 6_001_215,
}


def main() -> int:
    spark = get_spark("Verify TPC-H Iceberg Tables")

    print("\n=== Tables in lakehouse.tpch ===")
    spark.sql("SHOW TABLES IN lakehouse.tpch").show(truncate=False)

    print("\n=== Row counts vs expected (SF=1) ===")
    print(f"{'table':<10} {'actual':>12} {'expected':>12} {'status':>10}")
    print("-" * 50)

    all_ok = True
    for table, expected in EXPECTED_ROWS_SF1.items():
        try:
            actual = spark.table(f"lakehouse.tpch.{table}").count()
            status = "OK" if actual == expected else "MISMATCH"
            if actual != expected:
                all_ok = False
        except Exception as e:
            actual = "ERROR"
            status = f"FAIL: {type(e).__name__}"
            all_ok = False
        print(f"{table:<10} {str(actual):>12} {expected:>12} {status:>10}")

    print("\n=== Schema check (sample: lineitem) ===")
    spark.table("lakehouse.tpch.lineitem").printSchema()

    print("\n" + ("All tables verified." if all_ok else "Some tables missing/mismatched."))

    spark.stop()
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
