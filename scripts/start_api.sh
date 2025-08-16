#!/usr/bin/env bash
set -euo pipefail

# Move to repo root
cd "$(dirname "$0")/.."

# Load environment variables if .env exists
if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

PORT="${PORT:-8080}"

# Auto-run migrations (run from app/ so alembic.ini script_location resolves)
MIGRATE_ON_START="${MIGRATE_ON_START:-1}"
if [ "$MIGRATE_ON_START" = "1" ]; then
  (cd app && PYTHONPATH=.. uv run alembic upgrade head) || echo "[warn] Alembic migration failed; continuing startup"
fi

# Start API
export PYTHONPATH=.
exec uv run uvicorn app.main:app --host 0.0.0.0 --port "$PORT"


