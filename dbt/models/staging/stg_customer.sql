select
  cast(column0 as integer) as c_custkey,
  cast(column1 as varchar) as c_name,
  cast(column2 as varchar) as c_address,
  cast(column3 as integer) as c_nationkey,
  cast(column4 as varchar) as c_phone,
  cast(column5 as decimal(15,2)) as c_acctbal,
  cast(column6 as varchar) as c_mktsegment,
  cast(column7 as varchar) as c_comment
from {{ tpch_csv('customer') }}