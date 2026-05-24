#!/usr/bin/env bash
set -euo pipefail

# Get repository root path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "Stopping services and removing volumes..."
docker compose -f "${REPO_ROOT}/docker-compose.yml" down -v

echo "Cleaning up local data volumes..."
rm -rf "${REPO_ROOT}/data/minio"
rm -rf "${REPO_ROOT}/data/lakehouse"
rm -rf "${REPO_ROOT}/data/tpch"
mkdir -p "${REPO_ROOT}/data/minio" "${REPO_ROOT}/data/lakehouse" "${REPO_ROOT}/data/tpch"

echo "Starting services fresh..."
docker compose -f "${REPO_ROOT}/docker-compose.yml" up -d --build

echo "Clean reset complete!"
