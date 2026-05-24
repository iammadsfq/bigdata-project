from __future__ import annotations

from pyspark.sql import SparkSession


def get_spark(app_name: str, extra_conf: dict[str, str] | None = None) -> SparkSession:
    """Initialize a SparkSession using configurations from the environment and spark-defaults.conf.
    
    If additional/runtime configurations are needed (e.g. for benchmarking), they can be passed 
    via the extra_conf dictionary.
    """
    builder = SparkSession.builder.appName(app_name)
    if extra_conf:
        for key, value in extra_conf.items():
            builder = builder.config(key, value)
    return builder.getOrCreate()

