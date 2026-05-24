#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

SOURCE_DIR="${1:-${REPO_ROOT}/data/tpch}"
BUCKET="${2:-raw}"
PREFIX="${3:-tpch}"

if [[ ! -d "${SOURCE_DIR}" ]]; then
  echo "Source directory not found: ${SOURCE_DIR}"
  exit 1
fi

if ! compgen -G "${SOURCE_DIR}/*.csv" > /dev/null; then
  echo "No CSV files found in ${SOURCE_DIR}. Please run generate_tpch.sh first."
  exit 1
fi

# Ensure MinIO container is running
if [[ -z "$(docker ps --filter "name=minio" -q)" ]]; then
  echo "MinIO container not running. Start the stack: 'docker compose up -d'"
  exit 1
fi

echo "Uploading CSV files to MinIO (${BUCKET}/${PREFIX})..."

# Use docker compose run to mount source directory dynamically, auto-connecting to the network
docker compose run --rm \
  -v "${SOURCE_DIR}:/tpch:ro" \
  --entrypoint /bin/sh \
  minio-init \
  -c "mc alias set local http://minio:9000 minio minio123 && mc cp /tpch/*.csv local/${BUCKET}/${PREFIX}/"

echo "Upload complete."
