# Testing

## Unit / Integration
- Install dev deps: `uv sync`
- Run tests: `uv run pytest -q`
- Mark long-running tests as `@pytest.mark.integration` and deselect with `-m "not integration"`.

## What is covered
- Health endpoints
- Prompt loading
- Workflow with mocked Ollama
- Legacy workflow script tests

## Writing new tests
- Unit: isolate node logic; mock network/DB calls
- Integration: use FastAPI `TestClient`; run Celery worker if testing async flow
- Prefer asserts over prints/returns; keep tests small and focused

