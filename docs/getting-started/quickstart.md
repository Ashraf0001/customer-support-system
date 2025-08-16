# Quick Start

```bash
# Install
uv sync

# Run migrations
cd app && PYTHONPATH="$(dirname "$PWD")" uv run alembic upgrade head && cd ..

# Start API
DATABASE_HOST=localhost DATABASE_NAME=genai_launchpad DATABASE_USER=postgres \
DATABASE_PASSWORD=customer_support_password DATABASE_PORT=5432 \
OLLAMA_BASE_URL=http://localhost:11434 REDIS_URL=redis://127.0.0.1:6379/0 \
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080

# Submit a ticket
curl -X POST "http://localhost:8080/support/tickets" \
  -H "Content-Type: application/json" \
  -d '{"id":"test1","customer_email":"user@example.com","subject":"Login","content":"Cannot login","priority":"high"}'
```



