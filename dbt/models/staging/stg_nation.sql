select
  cast(column0 as integer) as n_nationkey,
  cast(column1 as varchar) as n_name,
  cast(column2 as integer) as n_regionkey,
  cast(column3 as varchar) as n_comment
from {{ tpch_csv('nation') }}