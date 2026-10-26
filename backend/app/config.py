import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")


class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL", "sqlite:///./database/buildlog.sqlite3"
    )
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
    backend_cors_origins: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "BACKEND_CORS_ORIGINS", "http://127.0.0.1:5173"
        ).split(",")
        if origin.strip()
    ]
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_KEY", "")


settings = Settings()
