#!/usr/bin/env bash
set -euo pipefail

SCALE="${1:-1}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
OUT_DIR="${2:-${REPO_ROOT}/data/tpch}"
DBGEN_DIR="${DBGEN_DIR:-${REPO_ROOT}/.dbgen}"
CLEAN_DBGEN="${CLEAN_DBGEN:-0}"

if ! command -v git >/dev/null 2>&1; then
  echo "git is required to clone tpch-dbgen."
  exit 1
fi
if ! command -v make >/dev/null 2>&1 || ! command -v gcc >/dev/null 2>&1; then
  echo "Local build tools are required (make + gcc)."
  exit 1
fi

if [[ "${CLEAN_DBGEN}" == "1" ]]; then
  rm -rf "${DBGEN_DIR}"
fi

if [[ ! -d "${DBGEN_DIR}/tpch-dbgen" ]]; then
  echo "Cloning tpch-dbgen into ${DBGEN_DIR}..."
  mkdir -p "${DBGEN_DIR}"
  git clone https://github.com/electrum/tpch-dbgen.git "${DBGEN_DIR}/tpch-dbgen"
fi

if [[ ! -x "${DBGEN_DIR}/tpch-dbgen/dbgen" ]]; then
  echo "Building dbgen locally..."
  (cd "${DBGEN_DIR}/tpch-dbgen" && make CC="gcc -std=gnu17 -fcommon -Wno-error=incompatible-pointer-types -Wno-error=implicit-function-declaration -Wno-error=int-conversion")
fi

mkdir -p "${OUT_DIR}"
rm -f "${OUT_DIR}"/*.tbl "${OUT_DIR}"/*.csv 2>/dev/null || true

echo "Generating TPC-H data locally (SF=${SCALE})..."

cd "${DBGEN_DIR}/tpch-dbgen"
rm -f ./*.tbl

./dbgen -s "${SCALE}" -f

shopt -s nullglob
for f in ./*.tbl; do
  sed -e 's/|$//' "$f" > "${OUT_DIR}/${f%.tbl}.csv"
done
shopt -u nullglob

if ! compgen -G "${OUT_DIR}/*.csv" > /dev/null; then
  echo "No CSV files were written to ${OUT_DIR}."
  exit 1
fi

echo "Done. Files are in ${OUT_DIR}"
