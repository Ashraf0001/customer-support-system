### Production Guide

This guide describes how to run the Customer Support System in production with a focus on reliability, security, and operability while keeping the MVP simple.

## Architecture (MVP)
- API (FastAPI/Uvicorn)
- Worker (Celery with Redis broker/result backend)
- Database (PostgreSQL)
- Local LLM (Ollama, e.g., `llama3.1:8b`)
- Optional reverse proxy (Nginx/Caddy) for TLS, routing, and limits

## Prerequisites
- Postgres 15+ reachable from API and Worker
- Redis 6+ reachable from API and Worker
- Ollama running where the Worker can reach it
  - Pull model once: `ollama pull llama3.1:8b`
  - Serve: `ollama serve` (port 11434 by default)
- A domain and TLS termination (e.g., Nginx/Caddy, or managed ingress)

## Required Environment Variables
Set these via your platform’s secret manager or a `.env` file (do not commit secrets):

```bash
# Project
PROJECT_NAME=customer_support_system

# Database
DATABASE_HOST=localhost
DATABASE_NAME=genai_launchpad
DATABASE_USER=postgres
DATABASE_PASSWORD=customer_support_password
DATABASE_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# API
PORT=8080

# Worker
CELERY_WORKER_CONCURRENCY=1  # tune per CPU/RAM
```

## Database Migrations
- Migrations must run before first start and on every deploy:
  - Using provided script: `./scripts/migrate.sh`
  - Or: `cd app && PYTHONPATH=.. uv run alembic upgrade head`
- Ensure indexes exist for common queries (`status`, `customer_email`) — included in the migrations.
- Backups: schedule `pg_dump` and verify restore regularly.

## Starting Services (Systemd example)
Below are minimalist systemd units for API and Worker. Adjust paths and users.

```ini
# /etc/systemd/system/customer-support-api.service
[Unit]
Description=Customer Support API
After=network.target

[Service]
WorkingDirectory=/srv/customer-support
EnvironmentFile=/srv/customer-support/.env
ExecStart=/usr/local/bin/uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/customer-support-worker.service
[Unit]
Description=Customer Support Celery Worker
After=network.target

[Service]
WorkingDirectory=/srv/customer-support
EnvironmentFile=/srv/customer-support/.env
ExecStart=/usr/local/bin/uv run celery -A app.worker.config.celery_app worker --loglevel=info -c ${CELERY_WORKER_CONCURRENCY}
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Reload and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now customer-support-api customer-support-worker
```

## Reverse Proxy (Nginx)
Terminate TLS and proxy to API:

```nginx
server {
  listen 443 ssl http2;
  server_name support.example.com;

  ssl_certificate /etc/letsencrypt/live/support.example.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/support.example.com/privkey.pem;

  client_max_body_size 2m;
  proxy_read_timeout 120s;

  location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

## CORS and UI
- The test UI is served at `/ui` by the API, ensuring same-origin and no CORS changes needed.
- If hosting the UI separately, either proxy it under the same domain or add CORS in code for that origin.

## Logging and Monitoring
- Logs: use JSON-friendly logs and ship to your aggregator
  - Uvicorn logs to stdout; capture via your process manager
  - Celery logs to stdout; capture similarly
- Health: expose `/healthz` and `/readyz`
- Metrics: start with request latency, error rate, Celery queue depth, task duration

## Security Hardening
- Only expose the API over HTTPS behind a proxy
- Keep Ollama bound to localhost or private network
- Rotate secrets; do not use defaults in production
- Rate-limit endpoints at the proxy
- Sanitize logs (no PII beyond what’s necessary)

## Scalability & Tuning
- API: scale processes/replicas at the proxy level
- Worker: set `CELERY_WORKER_CONCURRENCY` to match CPU/memory; consider multiple workers on a queue
- Database: use connection pooling (SQLAlchemy default); monitor CPU/IO; add indexes if needed
- Ollama: choose a model that fits memory; for low-RAM targets, consider `phi3:mini` as a drop-in

## Backup & Restore
```bash
# Backup
pg_dump -h $DATABASE_HOST -U $DATABASE_USER -d $DATABASE_NAME -Fc -f backup_$(date +%F).dump

# Restore
pg_restore -h $DATABASE_HOST -U $DATABASE_USER -d $DATABASE_NAME --clean backup_xxx.dump
```

## Deployment Checklist
- Application
  - [ ] `.env` created with production values
  - [ ] Alembic migrations applied
  - [ ] API and Worker started and healthy
  - [ ] `/ui` and `/docs` reachable (optional in prod)
- Platform
  - [ ] TLS enabled on reverse proxy
  - [ ] Rate limiting and basic WAF rules applied
  - [ ] Centralized logging in place
- Dependencies
  - [ ] Postgres reachable with correct creds
  - [ ] Redis reachable
  - [ ] Ollama running and model pulled

## CI/CD Essentials
- On every build: `uv run ruff check`, `uv run ruff format --check`, `uv run pyright`, `pytest`
- On deploy: run Alembic migrations; restart API and Worker with zero-downtime strategy

## Smoke Test (Post-Deploy)
```bash
curl -f https://support.example.com/healthz
curl -f -H 'Content-Type: application/json' -d '{
  "id":"smoke_test",
  "customer_email":"ops@example.com",
  "subject":"Health check",
  "content":"Ping",
  "priority":"low"
}' https://support.example.com/support/tickets
```




