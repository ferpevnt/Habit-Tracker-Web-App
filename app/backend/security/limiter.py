from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from config.config import settings

def get_user_or_ip(request: Request) -> str:
    token = request.cookies.get("access_token")

    if not token:
        return f"ip:{get_remote_address(request)}"
    try:
        token_data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = token_data.get("sub")
    except JWTError:
        return f"ip:{get_remote_address(request)}"

    if token_data.get("type") != "access":
        return f"ip:{get_remote_address(request)}"
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return f"ip:{get_remote_address(request)}"

    return f"user:{user_id}"

limiter = Limiter(
    key_func=get_user_or_ip,
    storage_uri=settings.REDIS_STORAGE_URI or None,
)
