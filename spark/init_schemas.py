from session import get_spark
spark = get_spark('Init')
spark.sql('CREATE DATABASE IF NOT EXISTS lakehouse.default')
spark.sql('CREATE DATABASE IF NOT EXISTS lakehouse.tpch_mart')
spark.stop()
