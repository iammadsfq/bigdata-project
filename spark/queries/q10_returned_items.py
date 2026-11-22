"""TPC-H Q10: Returned Item Reporting.

Four-way join (customer, orders, lineitem, nation) to find top
customers by lost revenue from returned items in a given quarter.
"""

from __future__ import annotations

from session import get_spark


QUERY = """
SELECT
    c_custkey,
    c_name,
    SUM(l_extendedprice * (1 - l_discount)) AS revenue,
    c_acctbal,
    n_name,
    c_address,
    c_phone,
    c_comment
FROM lakehouse.tpch.customer c
JOIN lakehouse.tpch.orders   o ON c.c_custkey   = o.o_custkey
JOIN lakehouse.tpch.lineitem l ON l.l_orderkey  = o.o_orderkey
JOIN lakehouse.tpch.nation   n ON c.c_nationkey = n.n_nationkey
WHERE o.o_orderdate >= DATE '1993-10-01'
  AND o.o_orderdate <  DATE '1994-01-01'
  AND l.l_returnflag = 'R'
GROUP BY c_custkey, c_name, c_acctbal, c_phone, n_name, c_address, c_comment
ORDER BY revenue DESC
LIMIT 20
"""


def main() -> int:
    spark = get_spark("TPC-H Q10 Returned Items")
    spark.sql(QUERY).show(truncate=False)
    spark.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
