#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "Stopping services and removing volumes..."
docker compose -f "${REPO_ROOT}/docker-compose.yml" down -v

echo "Cleaning up local data..."
if [[ -d "${REPO_ROOT}/data" ]]; then
  rm -rf "${REPO_ROOT}/data/minio" "${REPO_ROOT}/data/tpch" 2>/dev/null || \
    docker run --rm -v "${REPO_ROOT}/data:/data" alpine sh -c "rm -rf /data/minio /data/tpch"
fi
mkdir -p "${REPO_ROOT}/data/minio" "${REPO_ROOT}/data/tpch"

echo "Starting services fresh..."
docker compose -f "${REPO_ROOT}/docker-compose.yml" up -d --build

echo "Clean reset complete!"
