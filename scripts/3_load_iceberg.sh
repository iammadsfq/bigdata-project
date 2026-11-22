#!/usr/bin/env bash
set -euo pipefail

# Load TPC-H CSV tables from MinIO into Iceberg in a single Spark session.
# Optional args: specific table names (defaults to all 8 TPC-H tables).
docker compose exec -T spark /opt/spark/bin/spark-submit \
  /opt/spark/app/ingest/load_tables.py "$@"
