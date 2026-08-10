#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STORAGE_DIR="${ROOT_DIR}/backend/storage"

echo "========================================"
echo "Knowledge Assistant Storage Reset"
echo "========================================"
echo
echo "Storage directory:"
echo "${STORAGE_DIR}"
echo

if [[ ! -d "${STORAGE_DIR}" ]]; then
    echo "Storage directory does not exist."
    echo "Creating it..."
    mkdir -p "${STORAGE_DIR}"
    echo
    echo "Storage directory is ready."
    exit 0
fi

# ------------------------------------------------------------
# Require explicit confirmation
# ------------------------------------------------------------

if [[ "${1:-}" != "--force" ]]; then
    echo "WARNING: This will permanently delete all files"
    echo "inside:"
    echo
    echo "  ${STORAGE_DIR}"
    echo
    echo "This does NOT delete database records."
    echo "This does NOT delete migrations."
    echo "This does NOT delete application source code."
    echo
    echo "If you really want to continue, run:"
    echo
    echo "  ./scripts/reset_storage.sh --force"
    echo
    exit 1
fi

# ------------------------------------------------------------
# Reset storage
# ------------------------------------------------------------

echo "Resetting storage..."

find "${STORAGE_DIR}" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +

echo
echo "Storage reset completed successfully."
echo
echo "Storage directory:"
echo "${STORAGE_DIR}"