#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/backend"
FRONTEND_DIR="${ROOT_DIR}/frontend"

BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

echo "========================================"
echo "Starting Knowledge Assistant"
echo "========================================"
echo

# ------------------------------------------------------------
# Validate backend environment
# ------------------------------------------------------------

if [[ ! -x "${BACKEND_DIR}/.venv/bin/python" ]]; then
    echo "ERROR: Backend virtual environment was not found."
    echo
    echo "Run:"
    echo "  ./scripts/setup.sh"
    exit 1
fi

# ------------------------------------------------------------
# Validate frontend dependencies
# ------------------------------------------------------------

if [[ ! -d "${FRONTEND_DIR}/node_modules" ]]; then
    echo "ERROR: Frontend dependencies were not installed."
    echo
    echo "Run:"
    echo "  ./scripts/setup.sh"
    exit 1
fi

# ------------------------------------------------------------
# Cleanup function
# ------------------------------------------------------------

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo
    echo "Stopping Knowledge Assistant..."

    if [[ -n "${BACKEND_PID}" ]]; then
        kill "${BACKEND_PID}" 2>/dev/null || true
    fi

    if [[ -n "${FRONTEND_PID}" ]]; then
        kill "${FRONTEND_PID}" 2>/dev/null || true
    fi

    wait "${BACKEND_PID}" 2>/dev/null || true
    wait "${FRONTEND_PID}" 2>/dev/null || true

    echo "Application stopped."
}

trap cleanup SIGINT SIGTERM EXIT

# ------------------------------------------------------------
# Start backend
# ------------------------------------------------------------

echo "Starting FastAPI backend..."
echo "URL: http://localhost:${BACKEND_PORT}"
echo

cd "${BACKEND_DIR}"

"${BACKEND_DIR}/.venv/bin/python" -m uvicorn \
    app.main:app \
    --host 0.0.0.0 \
    --port "${BACKEND_PORT}" \
    --reload &

BACKEND_PID=$!

# ------------------------------------------------------------
# Start frontend
# ------------------------------------------------------------

echo "Starting React frontend..."
echo "URL: http://localhost:${FRONTEND_PORT}"
echo

cd "${FRONTEND_DIR}"

npm run dev -- --host 0.0.0.0 --port "${FRONTEND_PORT}" &

FRONTEND_PID=$!

# ------------------------------------------------------------
# Application information
# ------------------------------------------------------------

echo
echo "========================================"
echo "Knowledge Assistant is running"
echo "========================================"
echo
echo "Frontend:"
echo "  http://localhost:${FRONTEND_PORT}"
echo
echo "Backend:"
echo "  http://localhost:${BACKEND_PORT}"
echo
echo "API Documentation:"
echo "  http://localhost:${BACKEND_PORT}/docs"
echo
echo "Health:"
echo "  http://localhost:${BACKEND_PORT}/api/v1/health"
echo
echo "Press Ctrl+C to stop both services."
echo

# ------------------------------------------------------------
# Wait for either process
# ------------------------------------------------------------

wait -n "${BACKEND_PID}" "${FRONTEND_PID}"