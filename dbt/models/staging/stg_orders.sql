select
  cast(column0 as integer) as o_orderkey,
  cast(column1 as integer) as o_custkey,
  cast(column2 as varchar) as o_orderstatus,
  cast(column3 as decimal(15,2)) as o_totalprice,
  cast(column4 as date) as o_orderdate,
  cast(column5 as varchar) as o_orderpriority,
  cast(column6 as varchar) as o_clerk,
  cast(column7 as integer) as o_shippriority,
  cast(column8 as varchar) as o_comment
from {{ tpch_csv('orders') }}