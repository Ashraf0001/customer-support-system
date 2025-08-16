# Installation

## Prerequisites
- Python 3.12+
- uv (python package manager)
- Docker Desktop (Postgres & Redis), or local services
- Ollama with `llama3.1:8b`

## Steps
```bash
uv sync
# Start services (Postgres, Redis, Ollama)
cd app && PYTHONPATH="$(dirname "$PWD")" uv run alembic upgrade head && cd ..
DATABASE_HOST=localhost DATABASE_NAME=genai_launchpad DATABASE_USER=postgres \
DATABASE_PASSWORD=customer_support_password DATABASE_PORT=5432 \
OLLAMA_BASE_URL=http://localhost:11434 REDIS_URL=redis://127.0.0.1:6379/0 \
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080
```



