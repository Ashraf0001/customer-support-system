#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

cmd="${1:-upgrade}"
target="${2:-head}"

PYTHONPATH=. uv run alembic -c app/alembic.ini "$cmd" "$target"




