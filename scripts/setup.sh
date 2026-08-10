#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/backend"
FRONTEND_DIR="${ROOT_DIR}/frontend"

echo "========================================"
echo "Knowledge Assistant Development Setup"
echo "========================================"
echo

# ------------------------------------------------------------
# Check required commands
# ------------------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python 3 is required."
    exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
    echo "ERROR: npm is required."
    exit 1
fi

echo "Python: $(python3 --version)"
echo "Node:   $(node --version)"
echo "npm:    $(npm --version)"
echo

# ------------------------------------------------------------
# Backend setup
# ------------------------------------------------------------

echo "----------------------------------------"
echo "Setting up backend"
echo "----------------------------------------"

cd "${BACKEND_DIR}"

if [[ ! -d ".venv" ]]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
else
    echo "Python virtual environment already exists."
fi

PYTHON="${BACKEND_DIR}/.venv/bin/python"
PIP="${BACKEND_DIR}/.venv/bin/pip"

echo "Upgrading pip..."
"${PIP}" install --upgrade pip

echo "Installing backend dependencies..."
"${PIP}" install -r requirements.txt

# ------------------------------------------------------------
# Environment configuration
# ------------------------------------------------------------

if [[ ! -f ".env" ]]; then
    if [[ -f ".env.example" ]]; then
        echo "Creating backend .env from .env.example..."
        cp .env.example .env
    else
        echo "WARNING: backend/.env.example was not found."
    fi
else
    echo "Backend .env already exists."
fi

# ------------------------------------------------------------
# Local storage
# ------------------------------------------------------------

mkdir -p storage

echo
echo "Backend setup completed."

# ------------------------------------------------------------
# Frontend setup
# ------------------------------------------------------------

echo
echo "----------------------------------------"
echo "Setting up frontend"
echo "----------------------------------------"

cd "${FRONTEND_DIR}"

echo "Installing frontend dependencies..."

npm ci

if [[ ! -f ".env" && -f ".env.example" ]]; then
    echo "Creating frontend .env from .env.example..."
    cp .env.example .env
fi

echo
echo "Frontend setup completed."

# ------------------------------------------------------------
# Final output
# ------------------------------------------------------------

echo
echo "========================================"
echo "Development setup completed successfully"
echo "========================================"
echo
echo "Backend:"
echo "  ${BACKEND_DIR}/.venv"
echo
echo "Start the application with:"
echo "  ./scripts/start.sh"
echo