### Contributing

#### Branching
- Feature branches: `feature/<short-desc>`
- Fix branches: `fix/<short-desc>`

#### Commits (Conventional)
- `feat(api): add ticket submission endpoint`
- `fix(db): apply pool_pre_ping`

#### Quality checks
- Lint/format: `uv run ruff check --fix && uv run ruff format`
- Types: `uv run pyright`
- Tests: `uv run pytest`

#### PR checklist
- Description + rationale
- How to test
- No failing checks




