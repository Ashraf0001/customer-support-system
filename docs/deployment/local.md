# Local Deployment

## Option A: Dev scripts (recommended)
```bash
# From repo root
DATABASE_PASSWORD=customer_support_password ./scripts/start_api.sh
DATABASE_PASSWORD=customer_support_password ./scripts/start_worker.sh

# Open UI
open http://localhost:8080/ui
```

## Option B: Manual start
```bash
# 1) Migrate database
cd app && PYTHONPATH=.. uv run alembic upgrade head && cd ..

# 2) Start API
DATABASE_HOST=localhost DATABASE_NAME=genai_launchpad DATABASE_USER=postgres \
DATABASE_PASSWORD=customer_support_password DATABASE_PORT=5432 \
OLLAMA_BASE_URL=http://localhost:11434 REDIS_URL=redis://127.0.0.1:6379/0 \
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080

# 3) Start worker (new terminal)
DATABASE_PASSWORD=customer_support_password \
REDIS_URL=redis://127.0.0.1:6379/0 \
uv run celery -A app.worker.config.celery_app worker --loglevel=info -c 1
```

## Docker Compose
```bash
PROJECT_NAME=customer_support_system ./docker/start.sh
# API will be available at http://localhost:8080
```

## Health & Troubleshooting
- Health: `GET /healthz`, `GET /readyz`
- Logs: `tail -f /tmp/api.out`, `tail -f /tmp/worker.out`
- Common issues: see Deployment → Troubleshooting




