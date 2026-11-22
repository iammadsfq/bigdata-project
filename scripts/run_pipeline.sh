#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LOG_FILE="${REPO_ROOT}/pipeline_run.log"

exec > >(tee -i "${LOG_FILE}")
exec 2>&1

SCALE="${1:-1}"
OUT_DIR="${2:-${REPO_ROOT}/data/tpch}"

echo "=== [1/5] Generating TPC-H dataset (SF=${SCALE}) ==="
"${SCRIPT_DIR}/1_generate_tpch.sh" "${SCALE}" "${OUT_DIR}"

echo "=== [2/5] Uploading CSVs to MinIO ==="
"${SCRIPT_DIR}/2_upload_minio.sh" "${OUT_DIR}" raw tpch

echo "=== [3/5] Loading Iceberg tables ==="
"${SCRIPT_DIR}/3_load_iceberg.sh"

echo "=== [4/5] Running dbt transformations ==="
docker compose exec -T dbt dbt run

echo "=== [5/5] Running dbt data quality tests ==="
docker compose exec -T dbt dbt test

echo "=== Pipeline completed successfully! ==="
