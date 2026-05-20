#!/usr/bin/env bash
set -euo pipefail

SCALE="${1:-1}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUT_DIR="${2:-${REPO_ROOT}/data/tpch}"

bash "${SCRIPT_DIR}/dbgen/generate.sh" "${SCALE}" "${OUT_DIR}"
