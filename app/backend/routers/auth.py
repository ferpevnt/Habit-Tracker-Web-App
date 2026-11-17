from fastapi import APIRouter, Depends, Request, HTTPException, status, Response
from sqlalchemy.orm import Session
from database import database, models, schemas
from security.limiter import limiter
from security.security import hash_password, verify_password, create_access_token, get_current_user, verify_token
from config.config import settings

router = APIRouter(prefix="/auth", tags=["Authorization"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
@limiter.limit("2/minute")
@limiter.limit("3/hour")
def SignUp(
    user: schemas.UserCreate,
    request: Request,
    db: Session = Depends(database.get_db)):
    
    existing_email = db.query(
        models.User
    ).filter(
        models.User.email == user.email
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    password_hashed = hash_password(user.password)
    new_user = models.User(
        name = user.name,
        email = user.email,
        hashed_password = password_hashed
    )
    db.add(new_user)
    db.commit()

    return Response(status_code=status.HTTP_201_CREATED)

@router.post("/login")
@limiter.limit("3/minute")
@limiter.limit("5/hour")
def Login(
    user: schemas.UserLogin,
    request: Request,
    db: Session = Depends(database.get_db)):

    password = user.password
    user_data = db.query(
        models.User.id,
        models.User.hashed_password
    ).filter(
        models.User.email == user.email
    ).first()

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
        )

    password_check = verify_password(password, user_data.hashed_password)
    if not password_check:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
        )
    minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = create_access_token(user_data.id, minutes, "access")
    new_response = Response(status_code=status.HTTP_200_OK)
    new_response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,   #IMPORTANT: CHANGE WHEN DEPLOYMENT
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    
    refresh_token = create_access_token(user_data.id, settings.REFRESH_TOKEN_EXPIRE_MINUTES, "refresh") # lasts week
    new_response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
    )
    return new_response

@router.post("/refresh", status_code=status.HTTP_200_OK)
@limiter.limit("30/hour")
@limiter.limit("10/minute")
def RefreshToken(
    request: Request,
    db: Session=Depends(database.get_db)):
    
    user = verify_token(request, db, "refresh_token", "refresh")
    access_token = create_access_token(user.id, settings.ACCESS_TOKEN_EXPIRE_MINUTES, "access")
    new_response = Response(status_code=status.HTTP_200_OK)
    new_response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return new_response