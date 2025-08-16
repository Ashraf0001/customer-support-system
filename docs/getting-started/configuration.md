# Configuration

The app reads settings from environment variables. Key variables:

- `DATABASE_HOST`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_PORT`
- `REDIS_URL` (e.g., redis://127.0.0.1:6379/0)
- `OLLAMA_BASE_URL` (default: http://localhost:11434)
- `OLLAMA_MODEL` (default: llama3.1:8b)

All values are centralized in `app/core/config.py`.



