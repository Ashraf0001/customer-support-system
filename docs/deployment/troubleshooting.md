### Troubleshooting

#### API returns 500 on ticket submission: relation does not exist
- Cause: migrations not applied
- Fix: `./scripts/migrate.sh` or start via `./scripts/start_all.sh`

#### API returns 500: password authentication failed for user "postgres"
- Cause: `DATABASE_PASSWORD` mismatch
- Fix: export the correct password (defaults used in tests: `customer_support_password`) and restart API/worker

#### Worker fails with Ollama timeouts
- Cause: first call cold start; heavy model; high concurrency
- Fix: pull model, ensure `ollama serve` is running, use `phi3:mini`, set `CELERY_WORKER_CONCURRENCY=1`

#### Docs show ModuleNotFoundError: app
- Cause: mkdocstrings cannot import project
- Fix: run with `PYTHONPATH=.`, or use `./scripts/start_docs.sh`

#### Cannot connect to DB
- Verify `.env` `DATABASE_*` values
- Ensure Postgres is running and accessible

#### Retry endpoint returns 404
- Ticket ID not found; ensure it exists and is persisted (DB up and migrated)

#### Worker does not start: "exec: PYTHONPATH=.: not found"
- Cause: shell `exec` syntax
- Fix: use the provided `scripts/start_worker.sh` (exports `PYTHONPATH` before exec) or run the celery command directly




