#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

CONCURRENCY="${CELERY_WORKER_CONCURRENCY:-1}"

# Ensure DB is migrated before worker runs (run from app/ so alembic.ini resolves)
(cd app && PYTHONPATH=.. uv run alembic upgrade head)

# Ensure PYTHONPATH is exported for the exec'd process
PYTHONPATH=. exec uv run celery -A app.worker.config.celery_app worker --loglevel=info -c "$CONCURRENCY"


