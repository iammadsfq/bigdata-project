#!/usr/bin/env bash
set -euo pipefail

# Wrapper to invoke spark-submit inside the Spark container.
#
# Usage:
#   ./scripts/spark_submit.sh <python_file_in_/opt/spark/app> [args...]
#
# Example:
#   ./scripts/spark_submit.sh verify_tables.py
#   ./scripts/spark_submit.sh load_table.py customer

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <python_file> [args...]"
  exit 2
fi

APP_DIR="/opt/spark/app"
docker compose exec -T spark /opt/spark/bin/spark-submit \
  "${APP_DIR}/$1" "${@:2}"
