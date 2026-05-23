#!/usr/bin/env bash
set -euo pipefail

# Wrapper to invoke spark-submit inside the Spark container with the standard
# package set (Iceberg + Hadoop AWS + AWS SDK).
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
PACKAGES="org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0"

docker compose exec -T spark /opt/spark/bin/spark-submit \
  --packages "${PACKAGES}" \
  "${APP_DIR}/$1" "${@:2}"
