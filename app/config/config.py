import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)


def _require(key: str, example: str = "") -> str:
    value = os.getenv(key)
    if value is None or value == "":
        hint = f"\nPlease add to .env: {key}={example}" if example else ""
        raise ValueError(f"{key} is not set in .env!{hint}")
    return value


def _require_int(key: str, example: str = "") -> int:
    value = _require(key, example=example)
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{key} must be an integer, got: {value!r}")


def _require_bool(key: str) -> bool:
    value = _require(key, example="true")
    lower = value.strip().lower()
    if lower in ("true", "1", "yes"):
        return True
    if lower in ("false", "0", "no"):
        return False
    raise ValueError(f"{key} must be 'true' or 'false', got: {value!r}")


class Settings:

    # ===== DATABASE =====
    DATABASE_URL: str = _require(
        "DATABASE_URL",
        example="postgresql://user:pass@localhost:5432/db",
    )

    # ===== REDIS =====
    REDIS_STORAGE_URI: str = _require(
        "REDIS_STORAGE_URI",
        example="redis://localhost:6379",
    )

    # ===== CORS =====
    _allowed_raw: str = _require(
        "ALLOWED_ORIGINS",
        example="http://localhost:5500,http://127.0.0.1:5500",
    )
    ALLOWED_ORIGINS: list = [
        o.strip() for o in _allowed_raw.split(",") if o.strip()
    ]

    # ===== APP =====
    APP_NAME: str = os.getenv("APP_NAME", "My App")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

    # ===== AUTH (uncomment when needed) =====
    # SECRET_KEY: str = _require("SECRET_KEY", example="long_random_string")
    # ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = _require_int(
    #     "ACCESS_TOKEN_EXPIRE_MINUTES", example="30"
    # )
    # REFRESH_TOKEN_EXPIRE_DAYS: int = _require_int(
    #     "REFRESH_TOKEN_EXPIRE_DAYS", example="7"
    # )

    # ===== EMAIL (uncomment when needed) =====
    # MAIL_USERNAME: str = _require("MAIL_USERNAME", example="you@gmail.com")
    # MAIL_PASSWORD: str = _require("MAIL_PASSWORD", example="app_password")
    # MAIL_FROM: str = _require("MAIL_FROM", example="you@gmail.com")
    # MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "App")
    # MAIL_PORT: int = _require_int("MAIL_PORT", example="587")
    # MAIL_SERVER: str = _require("MAIL_SERVER", example="smtp.gmail.com")
    # MAIL_STARTTLS: bool = _require_bool("MAIL_STARTTLS")
    # MAIL_SSL_TLS: bool = _require_bool("MAIL_SSL_TLS")
    # USE_CREDENTIALS: bool = _require_bool("USE_CREDENTIALS")
    # VALIDATE_CERTS: bool = _require_bool("VALIDATE_CERTS")

    # ===== AI (uncomment when needed) =====
    # AI_API_KEY: str = _require("AI_API_KEY", example="your_api_key")
    # AI_MODEL: str = os.getenv("AI_MODEL", "gemini-1.5-flash")


settings = Settings()
