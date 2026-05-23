select
  cast(column00 as integer) as l_orderkey,
  cast(column01 as integer) as l_partkey,
  cast(column02 as integer) as l_suppkey,
  cast(column03 as integer) as l_linenumber,
  cast(column04 as decimal(15,2)) as l_quantity,
  cast(column05 as decimal(15,2)) as l_extendedprice,
  cast(column06 as decimal(15,2)) as l_discount,
  cast(column07 as decimal(15,2)) as l_tax,
  cast(column08 as varchar) as l_returnflag,
  cast(column09 as varchar) as l_linestatus,
  cast(column10 as date) as l_shipdate,
  cast(column11 as date) as l_commitdate,
  cast(column12 as date) as l_receiptdate,
  cast(column13 as varchar) as l_shipinstruct,
  cast(column14 as varchar) as l_shipmode,
  cast(column15 as varchar) as l_comment
from {{ tpch_csv('lineitem') }}