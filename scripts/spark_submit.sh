#!/usr/bin/env bash
set -euo pipefail

# Wrapper to invoke spark-submit inside the Spark container.
#
# Usage:
#   ./scripts/spark_submit.sh <relative_path_in_spark/> [args...]
#
# Examples:
#   ./scripts/spark_submit.sh ingest/verify_tables.py
#   ./scripts/spark_submit.sh queries/query_data_mart.py
#   ./scripts/spark_submit.sh benchmarks/benchmark_csv_vs_iceberg.py

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <relative_path_in_spark/> [args...]"
  exit 2
fi

APP_DIR="/opt/spark/app"
docker compose exec -T spark /opt/spark/bin/spark-submit \
  "${APP_DIR}/$1" "${@:2}"
