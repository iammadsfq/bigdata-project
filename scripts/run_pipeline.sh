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
PACKAGES="org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0"
docker compose exec -T spark /opt/spark/bin/spark-submit --packages "${PACKAGES}" /opt/spark/app/toy_query.py
