### Developer Guide (Intern Onboarding)

This guide helps you get productive quickly, even if you’re new to FastAPI, Celery, SQLAlchemy/Alembic, and Ollama.

#### What you’ll build
- Process support tickets: analyze → classify → generate AI response
- Stack: FastAPI API, Celery worker, PostgreSQL, Redis, Ollama LLM, SQLAlchemy, Alembic

#### 1) Prerequisites
- Python managed by uv (already configured)
- Docker (optional, for DB/Redis) or local Postgres/Redis
- Ollama installed and model pulled: `ollama pull phi3:mini` (or `llama3.1:8b`)

#### 2) Environment
- Create `.env` (no example committed) and set values for your machine
- Important vars: `DATABASE_*`, `REDIS_URL`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL`

Example `.env` for local dev:

```dotenv
PROJECT_NAME=customer_support_system

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

#### 3) One‑click scripts
- Start all: `./scripts/start_all.sh`
  - Runs migrations, starts API + Docs in background, Worker in foreground
- Start API only: `PORT=8080 ./scripts/start_api.sh`
- Start Worker only: `CELERY_WORKER_CONCURRENCY=1 ./scripts/start_worker.sh`
- Start Docs only: `DOCS_ADDR=127.0.0.1:9000 ./scripts/start_docs.sh`
- Stop all: `./scripts/stop_all.sh`
- Migrations: `./scripts/migrate.sh` (defaults to `upgrade head`)

#### 4) Where to look in the code
- API: `app/api/` (routes) and `app/main.py` (app startup, health)
- Workflows: `app/workflows/customer_support_*` and `app/core/workflow.py`
- Nodes: `app/workflows/customer_support_nodes/` (Analyze, Classify, Generate)
- Database: `app/database/` (models, session, repository)
- Schemas: `app/schemas/` (Pydantic request/response models)
- Worker: `app/worker/` (Celery config and tasks)
- Prompts: `app/prompts/` (prompt templates via Jinja2)
- Settings: `app/core/config.py` (centralized env-based config)
- UI: `app/static/index.html` (simple test console)

#### 5) Typical dev flow
1. Run `./scripts/start_all.sh`
2. Open API docs: http://127.0.0.1:8080/docs
3. Open UI: http://127.0.0.1:8080/ui
4. Submit a ticket from the UI, watch worker logs for processing

#### 6) Testing & Quality
- Run tests: `uv run pytest`
- Lint/format: `uv run ruff check --fix && uv run ruff format`
- Types: `uv run pyright`

Pre-commit (optional): configure hooks to run `ruff` and `pytest -q` before commits.

#### 7) Common pitfalls (quick)
- “relation support_tickets does not exist”: run migrations or use start scripts
- Ollama timeout on first call: expected; retries/backoff are in place; ensure model is pulled
- Auth/connection errors: ensure `.env` is loaded, DB/Redis running

If API starts but submit fails with 500: check `/tmp/api.out` and verify DB/Redis/Ollama reachability.

#### 8) What to change first
- Prompts under `app/prompts/` to tune AI outputs
- Node logic in `AnalyzeTicketNode` and `GenerateResponseNode`
- Simple classification thresholds or mapping in `ClassifyTicketNode`

You’re ready to contribute. For deeper explanations, see the other Development pages.




