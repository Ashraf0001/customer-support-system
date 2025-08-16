### AI & Ollama Integration

This project uses a local LLM via Ollama. No cloud keys required.

#### Setup
- Install Ollama (per official docs) and run `ollama serve`
- Pull a model, e.g.: `ollama pull phi3:mini` (lighter) or `ollama pull llama3.1:8b`
- Ensure `.env` contains `OLLAMA_BASE_URL` and `OLLAMA_MODEL`

#### How nodes call Ollama
- `AnalyzeTicketNode` → extracts `category`, `sentiment`, `urgency` from ticket
- `GenerateResponseNode` → produces a helpful response
- Both use HTTP POST to `OLLAMA_BASE_URL/api/generate`
- Retries with exponential backoff are applied to handle first-call slowness

#### Prompting
- Templates live in `app/prompts/`
- Use Jinja to insert ticket/context
- Output should be valid JSON only; avoid extra commentary to ease parsing

#### Common issues
- First call slow/timeout: expected warm-up; retries exist; try smaller model
- JSON parse errors: ensure prompt enforces JSON-only outputs; add guard parsing
- Memory limits: use `phi3:mini` or reduce concurrency (`CELERY_WORKER_CONCURRENCY=1`)

#### Tuning tips
- Keep prompts concise and explicit
- Prefer deterministic formatting over creative prose for machine parsing
- Log raw responses (already implemented) to refine prompts




