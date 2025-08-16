### Code Walkthrough

This is a guided tour of the core modules and how they work together.

#### Entry point: `app/main.py`
- Creates FastAPI app, registers routers, health endpoints
- Serves UI at `/ui` and redirects `/` → `/docs`
- Startup hook can warm up Ollama

#### API layer: `app/api/`
- `router.py`: aggregates sub-routers and health endpoints
- `customer_support_endpoint.py`:
  - Submit ticket: POST `/support/tickets`
  - List tickets: GET `/support/tickets`
  - Get ticket by id: GET `/support/tickets/{ticket_id}`
  - Retry processing: POST `/support/tickets/{ticket_id}/retry`

#### Schemas: `app/schemas/customer_support_schema.py`
- Pydantic models for input/output validation
- `SupportTicketSchema`, `SimpleClassificationSchema`, `ResponseSchema`

#### Database: `app/database/`
- `session.py`: SQLAlchemy engine/session setup (uses env settings)
- `support_ticket.py`: SQLAlchemy model (`support_tickets` table)
- `repository.py`: `GenericRepository` with `get`, `create`, `update`, `list`, `exists`

#### Alembic: `app/alembic/`
- `env.py`: configuration and metadata target for migrations
- `versions/*.py`: migration scripts (e.g., create `support_tickets`)
- Run via `./scripts/migrate.sh` or auto-run in start scripts

#### Worker & tasks: `app/worker/`
- `config.py`: Celery app and Redis config
- `tasks.py`: background processing for tickets; calls workflow

#### Core workflow engine: `app/core/workflow.py`
- Runs a sequence of Nodes with shared `TaskContext`
- Accepts event as dict or Pydantic model for flexibility

#### Customer support workflow: `app/workflows/customer_support_workflow.py`
- Declares node ordering and connections
- Primary nodes live under `app/workflows/customer_support_nodes/`

#### Nodes
- `AnalyzeTicketNode`: calls Ollama to extract category/sentiment/urgency
  - Retries with backoff; parses structured JSON from LLM output
- `ClassifyTicketNode`: lightweight rule-based or direct pass-through
- `GenerateResponseNode`: calls Ollama to produce response text

#### Prompts: `app/prompts/` and `app/services/prompt_loader.py`
- Simple Jinja templates to standardize system prompts
- Tip: keep outputs JSON-only to ease parsing

#### UI: `app/static/index.html`
- Minimal front-end to submit and monitor tickets
- Filters, retry, error display, copy/download AI response

#### Settings: `app/core/config.py`
- Centralized env-based settings (DB, Redis, Ollama)

#### Logging
- Node-level logs indicate start/finish and status
- Errors include context (e.g., raw Ollama text on parse failure)

Use this walkthrough while reading the code to speed up comprehension.




