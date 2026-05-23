with customer as (
  select * from {{ ref('stg_customer') }}
),
orders as (
  select * from {{ ref('stg_orders') }}
),
lineitem as (
  select * from {{ ref('stg_lineitem') }}
),
nation as (
  select * from {{ ref('stg_nation') }}
)

select
  c.c_custkey,
  c.c_name,
  sum(l.l_extendedprice * (1 - l.l_discount)) as revenue,
  c.c_acctbal,
  n.n_name,
  c.c_address,
  c.c_phone,
  c.c_comment
from customer c
join orders o on c.c_custkey = o.o_custkey
join lineitem l on l.l_orderkey = o.o_orderkey
join nation n on c.c_nationkey = n.n_nationkey
where o.o_orderdate >= date '1993-10-01'
  and o.o_orderdate < date '1994-01-01'
  and l.l_returnflag = 'R'
group by
  c.c_custkey, c.c_name, c.c_acctbal, n.n_name, c.c_address, c.c_phone, c.c_comment
order by revenue desc