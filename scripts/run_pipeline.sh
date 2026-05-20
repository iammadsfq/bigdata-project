#!/usr/bin/env bash
set -euo pipefail

SCALE="${1:-1}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUT_DIR="${2:-${REPO_ROOT}/data/tpch}"

bash "${SCRIPT_DIR}/generate_tpch.sh" "${SCALE}" "${OUT_DIR}"
bash "${SCRIPT_DIR}/minio/upload.sh" "${OUT_DIR}" raw tpch
bash "${SCRIPT_DIR}/load_to_iceberg.sh"

echo "Running toy query..."
docker compose exec -T spark /opt/spark/bin/spark-submit /opt/spark/app/toy_query.py
