#!/usr/bin/env bash
set -euo pipefail

# Redirect all output to a log file but also display it
LOG_FILE="pipeline_run.log"
exec > >(tee -i "${LOG_FILE}")
exec 2>&1

SCALE="${1:-1}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUT_DIR="${2:-${REPO_ROOT}/data/tpch}"

bash "${SCRIPT_DIR}/generate_tpch.sh" "${SCALE}" "${OUT_DIR}"
bash "${SCRIPT_DIR}/minio/upload.sh" "${OUT_DIR}" raw tpch
bash "${SCRIPT_DIR}/load_to_iceberg.sh"

echo "Running dbt transformations..."
docker compose exec -T dbt dbt run --profiles-dir . --project-dir .

echo "Running dbt data quality tests..."
docker compose exec -T dbt dbt test --profiles-dir . --project-dir .
