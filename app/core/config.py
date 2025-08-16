import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    """Centralized application settings loaded from environment.

    Uses simple environment lookups to avoid extra dependencies.
    """

    project_name: str = os.getenv("PROJECT_NAME", "customer_support_system")

    # Database
    database_host: str = os.getenv("DATABASE_HOST", "localhost")
    database_name: str = os.getenv("DATABASE_NAME", "genai_launchpad")
    database_user: str = os.getenv("DATABASE_USER", "postgres")
    database_password: str = os.getenv("DATABASE_PASSWORD", "postgres")
    database_port: str = os.getenv("DATABASE_PORT", "5432")

    # Redis / Celery
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Ollama
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    # Paths
    base_dir: Path = Path(__file__).resolve().parent.parent


settings = Settings()






