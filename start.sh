#!/usr/bin/env bash
set -euo pipefail

export PYTHONUNBUFFERED=1

# Load backend .env if present (at /usr/src/.env)
if [ -f "/usr/src/.env" ]; then
  echo "Loading backend env from /usr/src/.env"
  set -a
  . /usr/src/.env
  set +a
fi

# Start frontend in background
cd /usr/src/tripplanner

# Load frontend .env if present (at /usr/src/tripplanner/.env)
if [ -f "/usr/src/tripplanner/.env" ]; then
  echo "Loading frontend env from /usr/src/tripplanner/.env"
  set -a
  . /usr/src/tripplanner/.env
  set +a
fi
if [ -n "${FRONTEND_DEV_ARGS:-}" ]; then
  echo "Starting frontend: npm run dev ${FRONTEND_DEV_ARGS}"
  npm run dev -- ${FRONTEND_DEV_ARGS} &
else
  echo "Starting frontend: npm run dev"
  npm run dev &
fi
FRONTEND_PID=$!

cleanup() {
  if ps -p ${FRONTEND_PID} > /dev/null 2>&1; then
    echo "Stopping frontend (PID ${FRONTEND_PID})"
    kill ${FRONTEND_PID} || true
  fi
}
trap cleanup EXIT

# Start backend in foreground
cd /usr/src
echo "Starting backend: uvicorn app.main:app on ${BACKEND_HOST:-0.0.0.0}:${BACKEND_PORT:-8000}"
exec /opt/venv/bin/python -m uvicorn app.main:app \
  --host "${BACKEND_HOST:-0.0.0.0}" \
  --port "${BACKEND_PORT:-8000}" \
  --reload
