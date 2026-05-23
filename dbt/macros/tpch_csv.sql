{% macro tpch_csv(table_name) -%}
read_csv_auto('/work/data/tpch/{{ table_name }}.csv', delim='|', header=false, all_varchar=true)
{%- endmacro %}