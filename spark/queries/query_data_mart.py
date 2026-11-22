"""Query the dbt Data Mart (lakehouse.tpch_mart.fct_customer_revenue) using PySpark."""

from __future__ import annotations

from session import get_spark


def main() -> int:
    spark = get_spark("Query dbt Data Mart")
    spark.sparkContext.setLogLevel("WARN")

    print("\n=== Checking for Data Mart Table ===")
    mart_table = "lakehouse.tpch_mart.fct_customer_revenue"
    
    try:
        # Check if table exists by reading its metadata
        df = spark.table(mart_table)
        print(f"  Table '{mart_table}' found successfully.")
    except Exception as e:
        print(f"\n  ERROR: Could not load table '{mart_table}': {e}")
        print("  Please make sure you run the dbt pipeline first to build the mart:")
        print("    docker compose exec dbt dbt run")
        spark.stop()
        return 1

    print("\n=== Data Mart Schema ===")
    df.printSchema()

    print("\n=== Data Mart Row Count ===")
    try:
        row_count = df.count()
        print(f"  Total Rows: {row_count:,}")
    except Exception as e:
        print(f"  Error counting rows: {e}")
        spark.stop()
        return 1

    print("\n=== Top 20 Customers by Revenue (Data Mart Preview) ===")
    try:
        # Show top 20 rows (no truncation for string columns like comment/address)
        df.show(20, truncate=False)
    except Exception as e:
        print(f"  Error retrieving data: {e}")
        spark.stop()
        return 1

    spark.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
