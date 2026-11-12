# Password hashing / JWT helpers.
# Uncomment and use when auth is implemented.

# from passlib.context import CryptContext
# from jose import jwt, JWTError
# from datetime import datetime, timedelta, timezone
# from config.config import settings
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)
#
# def verify_password(plain: str, hashed: str) -> bool:
#     return pwd_context.verify(plain, hashed)
