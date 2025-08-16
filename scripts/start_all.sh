#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

# Run migrations first
PYTHONPATH=. uv run alembic -c app/alembic.ini upgrade head

# Start API and Docs in background; Worker in foreground for logs
./scripts/start_api.sh &
API_PID=$!

./scripts/start_docs.sh &
DOCS_PID=$!

trap 'kill $API_PID $DOCS_PID 2>/dev/null || true' EXIT

./scripts/start_worker.sh




