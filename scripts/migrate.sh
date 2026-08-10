#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/backend"

echo "========================================"
echo "Knowledge Assistant Database Migration"
echo "========================================"
echo

if [[ ! -d "${BACKEND_DIR}" ]]; then
    echo "ERROR: Backend directory not found:"
    echo "${BACKEND_DIR}"
    exit 1
fi

cd "${BACKEND_DIR}"

# ------------------------------------------------------------
# Select Python environment
# ------------------------------------------------------------

if [[ -x "${BACKEND_DIR}/.venv/bin/python" ]]; then
    PYTHON="${BACKEND_DIR}/.venv/bin/python"
else
    PYTHON="python3"
fi

echo "Backend: ${BACKEND_DIR}"
echo "Python:  ${PYTHON}"
echo

# ------------------------------------------------------------
# Verify Alembic is available
# ------------------------------------------------------------

if ! "${PYTHON}" -m alembic --version > /dev/null 2>&1; then
    echo "ERROR: Alembic is not installed in the selected Python environment."
    echo
    echo "Install backend dependencies first:"
    echo "  pip install -r backend/requirements.txt"
    exit 1
fi

# ------------------------------------------------------------
# Verify Alembic configuration
# ------------------------------------------------------------

if [[ ! -f "${BACKEND_DIR}/alembic.ini" ]]; then
    echo "ERROR: alembic.ini not found:"
    echo "${BACKEND_DIR}/alembic.ini"
    exit 1
fi

if [[ ! -d "${BACKEND_DIR}/migrations" ]]; then
    echo "ERROR: migrations directory not found:"
    echo "${BACKEND_DIR}/migrations"
    exit 1
fi

# ------------------------------------------------------------
# Run migrations
# ------------------------------------------------------------

echo "Running database migrations..."
echo

"${PYTHON}" -m alembic upgrade head

echo
echo "========================================"
echo "Database migration completed successfully."
echo "========================================"