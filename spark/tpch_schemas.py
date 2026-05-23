from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    LongType,
    StringType,
    DecimalType,
    DateType,
)


_DECIMAL = DecimalType(15, 2)


REGION_SCHEMA = StructType([
    StructField("r_regionkey", IntegerType(), False),
    StructField("r_name",      StringType(),  False),
    StructField("r_comment",   StringType(),  True),
])


NATION_SCHEMA = StructType([
    StructField("n_nationkey", IntegerType(), False),
    StructField("n_name",      StringType(),  False),
    StructField("n_regionkey", IntegerType(), False),
    StructField("n_comment",   StringType(),  True),
])


SUPPLIER_SCHEMA = StructType([
    StructField("s_suppkey",   IntegerType(), False),
    StructField("s_name",      StringType(),  False),
    StructField("s_address",   StringType(),  False),
    StructField("s_nationkey", IntegerType(), False),
    StructField("s_phone",     StringType(),  False),
    StructField("s_acctbal",   _DECIMAL,      False),
    StructField("s_comment",   StringType(),  True),
])


CUSTOMER_SCHEMA = StructType([
    StructField("c_custkey",    IntegerType(), False),
    StructField("c_name",       StringType(),  False),
    StructField("c_address",    StringType(),  False),
    StructField("c_nationkey",  IntegerType(), False),
    StructField("c_phone",      StringType(),  False),
    StructField("c_acctbal",    _DECIMAL,      False),
    StructField("c_mktsegment", StringType(),  False),
    StructField("c_comment",    StringType(),  True),
])


PART_SCHEMA = StructType([
    StructField("p_partkey",     IntegerType(), False),
    StructField("p_name",        StringType(),  False),
    StructField("p_mfgr",        StringType(),  False),
    StructField("p_brand",       StringType(),  False),
    StructField("p_type",        StringType(),  False),
    StructField("p_size",        IntegerType(), False),
    StructField("p_container",   StringType(),  False),
    StructField("p_retailprice", _DECIMAL,      False),
    StructField("p_comment",     StringType(),  True),
])


PARTSUPP_SCHEMA = StructType([
    StructField("ps_partkey",    IntegerType(), False),
    StructField("ps_suppkey",    IntegerType(), False),
    StructField("ps_availqty",   IntegerType(), False),
    StructField("ps_supplycost", _DECIMAL,      False),
    StructField("ps_comment",    StringType(),  True),
])


ORDERS_SCHEMA = StructType([
    StructField("o_orderkey",      LongType(),    False),
    StructField("o_custkey",       IntegerType(), False),
    StructField("o_orderstatus",   StringType(),  False),
    StructField("o_totalprice",    _DECIMAL,      False),
    StructField("o_orderdate",     DateType(),    False),
    StructField("o_orderpriority", StringType(),  False),
    StructField("o_clerk",         StringType(),  False),
    StructField("o_shippriority",  IntegerType(), False),
    StructField("o_comment",       StringType(),  True),
])


LINEITEM_SCHEMA = StructType([
    StructField("l_orderkey",      LongType(),    False),
    StructField("l_partkey",       IntegerType(), False),
    StructField("l_suppkey",       IntegerType(), False),
    StructField("l_linenumber",    IntegerType(), False),
    StructField("l_quantity",      _DECIMAL,      False),
    StructField("l_extendedprice", _DECIMAL,      False),
    StructField("l_discount",      _DECIMAL,      False),
    StructField("l_tax",           _DECIMAL,      False),
    StructField("l_returnflag",    StringType(),  False),
    StructField("l_linestatus",    StringType(),  False),
    StructField("l_shipdate",      DateType(),    False),
    StructField("l_commitdate",    DateType(),    False),
    StructField("l_receiptdate",   DateType(),    False),
    StructField("l_shipinstruct",  StringType(),  False),
    StructField("l_shipmode",      StringType(),  False),
    StructField("l_comment",       StringType(),  True),
])


SCHEMAS = {
    "region":   REGION_SCHEMA,
    "nation":   NATION_SCHEMA,
    "supplier": SUPPLIER_SCHEMA,
    "customer": CUSTOMER_SCHEMA,
    "part":     PART_SCHEMA,
    "partsupp": PARTSUPP_SCHEMA,
    "orders":   ORDERS_SCHEMA,
    "lineitem": LINEITEM_SCHEMA,
}
