#!/usr/bin/env bash

set -euo pipefail

BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
HEALTH_ENDPOINT="${BACKEND_URL}/api/v1/health"

echo "========================================"
echo "Knowledge Assistant Health Check"
echo "========================================"
echo
echo "Checking: ${HEALTH_ENDPOINT}"
echo

if curl --fail --silent --show-error \
    --connect-timeout 5 \
    --max-time 10 \
    "${HEALTH_ENDPOINT}" > /tmp/knowledge-assistant-health.json; then

    echo "Backend: OK"
    echo
    cat /tmp/knowledge-assistant-health.json
    echo
    echo
    echo "Health check passed."

    rm -f /tmp/knowledge-assistant-health.json
    exit 0

else

    echo "Backend: FAILED"
    echo
    echo "Unable to reach:"
    echo "${HEALTH_ENDPOINT}"
    echo
    echo "Make sure the backend is running and the URL is correct."

    rm -f /tmp/knowledge-assistant-health.json
    exit 1
fi