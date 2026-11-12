from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from config.config import settings


def get_user_or_ip(request: Request) -> str:
    """
    Key for rate limiting.
    For now — just IP. Replace with user_id (from JWT/cookie) when auth is ready.
    """
    return f"ip:{get_remote_address(request)}"


limiter = Limiter(
    key_func=get_user_or_ip,
    storage_uri=settings.REDIS_STORAGE_URI or None,
)
