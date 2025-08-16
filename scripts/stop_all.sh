#!/usr/bin/env bash
set -euo pipefail

# Stop API, worker, docs started via uv run
pkill -f "uv run uvicorn app.main:app" || true
pkill -f "uv run celery -A app.worker.config.celery_app" || true
pkill -f "uv run mkdocs serve" || true

echo "Stopped API, worker, and docs (if running)."




