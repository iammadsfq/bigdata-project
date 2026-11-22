"""TPC-H Q3: Shipping Priority.

Three-way join (customer, orders, lineitem) to find top revenue
orders that haven't shipped yet for a given market segment.
"""

from __future__ import annotations

from session import get_spark


QUERY = """
SELECT
    l_orderkey,
    SUM(l_extendedprice * (1 - l_discount)) AS revenue,
    o_orderdate,
    o_shippriority
FROM lakehouse.tpch.customer c
JOIN lakehouse.tpch.orders   o ON c.c_custkey  = o.o_custkey
JOIN lakehouse.tpch.lineitem l ON l.l_orderkey = o.o_orderkey
WHERE c.c_mktsegment = 'BUILDING'
  AND o.o_orderdate < DATE '1995-03-15'
  AND l.l_shipdate  > DATE '1995-03-15'
GROUP BY l_orderkey, o_orderdate, o_shippriority
ORDER BY revenue DESC, o_orderdate
LIMIT 10
"""


def main() -> int:
    spark = get_spark("TPC-H Q3 Shipping Priority")
    spark.sql(QUERY).show(truncate=False)
    spark.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
