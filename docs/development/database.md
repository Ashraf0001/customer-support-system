### Database & Migrations

#### ORM & Models
- SQLAlchemy is used for models and sessions
- Main model: `SupportTicket` in `app/database/support_ticket.py`

#### Sessions
- Created in `app/database/session.py` with `pool_pre_ping=True`
- Use the repository pattern (`app/database/repository.py`) inside API and worker

#### Migrations
- Alembic configs in `app/alembic/` (and `app/alembic.ini`)
- Run migrations:
  - `./scripts/migrate.sh` (default upgrade head)
  - or auto-run via `./scripts/start_api.sh` / `./scripts/start_worker.sh`

#### Troubleshooting
- “relation support_tickets does not exist” → run migrations
- Auth errors → verify `.env` DB creds; ensure Postgres is running
- Stale connections → `pool_pre_ping=True` mitigates; restart services if needed




