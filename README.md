# Customer Support System

GenAI-powered customer support workflow built on FastAPI, Celery, PostgreSQL, Redis, and a local LLM (Ollama). MVP scope: Analyze ticket → Simple classify → Generate response.

## Features
- Support ticket submission API (`POST /support/tickets`)
- Async processing via Celery worker
- Local LLM (Ollama) integration for analysis and response
- Simple UI at `/ui` for quick manual testing
- Typed models (Pydantic), migrations (Alembic)

## Architecture
- API: FastAPI (Uvicorn)
- Worker: Celery with Redis broker/result backend
- DB: PostgreSQL (`support_tickets` table)
- LLM: Ollama (default `llama3.1:8b`)

## Quick Start (Local)
```bash
# 1) Install deps
uv sync

# 2) Start API
DATABASE_PASSWORD=customer_support_password ./scripts/start_api.sh

# 3) Start Worker
DATABASE_PASSWORD=customer_support_password ./scripts/start_worker.sh

# 4) Open UI
open http://localhost:8080/ui
```

Requirements:
- Postgres on localhost:5432 (db: genai_launchpad / user: postgres / pass: customer_support_password)
- Redis on localhost:6379
- Ollama on localhost:11434 with model pulled: `ollama pull llama3.1:8b`

## Environment Variables
```bash
DATABASE_HOST=localhost
DATABASE_NAME=genai_launchpad
DATABASE_USER=postgres
DATABASE_PASSWORD=customer_support_password
DATABASE_PORT=5432
REDIS_URL=redis://127.0.0.1:6379/0
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
PORT=8080
CELERY_WORKER_CONCURRENCY=1
```

## API Endpoints (Core)
- `POST /support/tickets` → Accepts a ticket (202 Accepted) and queues processing
- `GET /support/tickets` → Lists tickets with optional filters
- `GET /support/tickets/{id}` → Ticket details
- `POST /support/tickets/{id}/retry` → Re-queue a failed ticket
- Health: `/healthz`, `/readyz`

Example submit:
```bash
curl -X POST "http://localhost:8080/support/tickets" \
  -H "Content-Type: application/json" \
  -d '{
        "id":"test123",
        "customer_email":"user@example.com",
        "subject":"Login issue",
        "content":"Cannot login",
        "priority":"high"
      }'
```

## Documentation
- Local docs: `uv run mkdocs serve` (open the served URL)
- Static build: `uv run mkdocs build` (outputs to `site/`)
- Key guides: see `docs/deployment/production.md` for production hardening and checklist

## Production (Essentials)
- Run Alembic migrations on deploy
- Secure env vars (no defaults)
- Put API behind TLS (reverse proxy)
- Keep Ollama private (local or private network)
- Monitor worker queue depth and task duration

## Project Structure
```text
app/                 # API, models, workflows, worker tasks
docs/                # MkDocs site (developer + deployment docs)
scripts/             # Start and helper scripts
docker/              # Optional compose & Dockerfiles
```

## License
See [LICENSE](LICENSE).

---

For details and advanced usage, read the docs under `docs/`.
