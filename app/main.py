from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.core.config import settings
from app.api.router import router as process_router

def _prewarm_ollama():
    # Fire-and-forget lightweight warmup
    try:
        import requests
        requests.get(f"{settings.ollama_base_url}/api/tags", timeout=3)
    except Exception:
        pass

app = FastAPI()
app.include_router(process_router)

_prewarm_ollama()

# Serve a simple web UI for manual testing at /ui
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/ui", StaticFiles(directory=str(static_dir), html=True), name="ui")
