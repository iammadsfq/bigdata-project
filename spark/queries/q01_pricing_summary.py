"""TPC-H Q1: Pricing Summary Report.

Aggregation over the entire lineitem table, filtered by shipdate.
Reports revenue, discount, and tax summaries grouped by return flag
and line status.
"""

from __future__ import annotations

from session import get_spark


QUERY = """
SELECT
    l_returnflag,
    l_linestatus,
    SUM(l_quantity)                                        AS sum_qty,
    SUM(l_extendedprice)                                   AS sum_base_price,
    SUM(l_extendedprice * (1 - l_discount))                AS sum_disc_price,
    SUM(l_extendedprice * (1 - l_discount) * (1 + l_tax))  AS sum_charge,
    AVG(l_quantity)                                        AS avg_qty,
    AVG(l_extendedprice)                                   AS avg_price,
    AVG(l_discount)                                        AS avg_disc,
    COUNT(*)                                               AS count_order
FROM lakehouse.tpch.lineitem
WHERE l_shipdate <= DATE '1998-09-02'
GROUP BY l_returnflag, l_linestatus
ORDER BY l_returnflag, l_linestatus
"""


def main() -> int:
    spark = get_spark("TPC-H Q1 Pricing Summary")
    spark.sql(QUERY).show(truncate=False)
    spark.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
