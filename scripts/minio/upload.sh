#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

SOURCE_DIR="${1:-${REPO_ROOT}/data/tpch}"
BUCKET="${2:-raw}"
PREFIX="${3:-tpch}"
NETWORK="${4:-bigdata-project_default}"
MC_CONFIG_DIR="${REPO_ROOT}/.mc"

if [[ ! -d "${SOURCE_DIR}" ]]; then
  echo "Source directory not found: ${SOURCE_DIR}"
  exit 1
fi

TARGET="local/${BUCKET}/${PREFIX}"

echo "Uploading CSV files to MinIO -> ${TARGET}"

mkdir -p "${MC_CONFIG_DIR}"

if ! compgen -G "${SOURCE_DIR}/*.csv" > /dev/null; then
  echo "No CSV files found in ${SOURCE_DIR}"
  exit 1
fi

# Ensure MinIO is running (easy check)
if [[ -z "$(docker ps --filter "name=minio" -q)" ]]; then
  echo "MinIO container not running. Start the stack: 'docker compose up -d'"
  exit 1
fi

# Set alias (runs mc as the container entrypoint)
docker run --rm --network "${NETWORK}" \
  -v "${MC_CONFIG_DIR}:/config" \
  minio/mc:latest \
  --config-dir /config alias set local http://minio:9000 minio minio123

# Create the bucket/prefix if it doesn't exist (ignore errors if it already exists)
docker run --rm --network "${NETWORK}" \
  -v "${MC_CONFIG_DIR}:/config" \
  minio/mc:latest \
  --config-dir /config mb -p "${TARGET}" || true

# Copy CSVs from the mounted host directory into the target
docker run --rm --network "${NETWORK}" \
  -v "${SOURCE_DIR}:/data" \
  -v "${MC_CONFIG_DIR}:/config" \
  -e TARGET="${TARGET}" \
  --entrypoint /bin/sh \
  minio/mc:latest \
  -c 'set -e; mc --config-dir /config cp /data/*.csv "$TARGET/"'

echo "Upload complete."
