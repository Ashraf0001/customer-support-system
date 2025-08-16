#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

ADDR="${DOCS_ADDR:-127.0.0.1:9000}"

export PYTHONPATH=.
exec uv run mkdocs serve -a "$ADDR"


