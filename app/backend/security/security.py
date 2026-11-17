from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from config.config import settings
from database import database, models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: int, minutes_amount: int, token_type: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes_amount)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": token_type
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(request, db, token_type, expected_type):
    token = request.cookies.get(token_type)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"})
    try:
        token_data = jwt.decode(
            token, 
            settings.SECRET_KEY,
            algorithms = [settings.ALGORITHM])
        user_id = token_data.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"})
    if token_data.get("type") != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong token type",
            headers={"WWW-Authenticate": "Bearer"})
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong user id type",
            headers={"WWW-Authenticate": "Bearer"})

    user = db.query(
        models.User
        ).filter(
            models.User.id == user_id
        ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with such id not found",
            headers={"WWW-Authenticate": "Bearer"})
    return user

def get_current_user(request: Request, db: Session=Depends(database.get_db)) -> models.User:
    return verify_token(request, db, "access_token", "access")