# Architecture

## Overview
- FastAPI for API and docs
- Celery + Redis for async tasks
- PostgreSQL via SQLAlchemy and Alembic
- Ollama for local LLM calls

## Components
- API: `app/api/*`, `app/main.py`
- Workflow: `app/core/workflow.py`, `app/workflows/*`
- Nodes: `app/workflows/customer_support_nodes/*`
- DB: `app/database/*`
- Worker: `app/worker/*`
- Schemas: `app/schemas/*`
- Prompts: `app/prompts/*`
- UI: `app/static/index.html`

## Data flow
1. Client submits ticket to API
2. API persists ticket to DB (status=open) and enqueues Celery task
3. Worker runs workflow nodes (analyze → classify → generate)
4. Worker updates ticket with results (status=resolved or failed)
5. UI polls `/support/tickets` for updates

