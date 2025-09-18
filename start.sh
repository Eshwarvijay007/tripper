#!/usr/bin/env bash
set -euo pipefail
export PYTHONUNBUFFERED=1

# Load backend .env
if [ -f "/usr/src/.env" ]; then
  set -a
  . /usr/src/.env
  set +a
fi

# Load frontend .env (for API keys etc. baked into React build)
if [ -f "/usr/src/tripplanner/.env" ]; then
  set -a
  . /usr/src/tripplanner/.env
  set +a
fi

echo "Starting backend: uvicorn app.main:app on 0.0.0.0:${PORT:-8080}"
exec /opt/venv/bin/python -m uvicorn app.main:app \
  --host 0.0.0.0 \
  --port "${PORT:-8080}"
