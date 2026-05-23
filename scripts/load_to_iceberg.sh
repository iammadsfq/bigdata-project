#!/usr/bin/env bash
set -euo pipefail

TABLES=(region nation supplier customer part partsupp orders lineitem)
APP_DIR="/opt/spark/app"
PACKAGES="org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0"

for table in "${TABLES[@]}"; do
  echo "Loading ${table} into Iceberg..."
  docker compose exec -T spark /opt/spark/bin/spark-submit --packages "${PACKAGES}" "${APP_DIR}/load_table.py" "${table}"
done

echo "Iceberg load complete."
