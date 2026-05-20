#!/usr/bin/env bash
set -euo pipefail

TABLES=(customer orders lineitem)
APP_DIR="/opt/spark/app"

for table in "${TABLES[@]}"; do
  echo "Loading ${table} into Iceberg..."
  docker compose exec -T spark /opt/spark/bin/spark-submit "${APP_DIR}/load_table.py" "${table}"
done

echo "Iceberg load complete."
