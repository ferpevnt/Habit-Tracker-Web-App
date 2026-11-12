from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import database, models, schemas
from security.limiter import limiter
from typing import List

router = APIRouter(prefix="/examples", tags=["Examples"])


# ===== EXAMPLE ROUTER (delete me) =====

@router.get("/", response_model=List[schemas.ExampleOut])
@limiter.limit("60/minute")
def list_examples(
    request: Request,
    db: Session = Depends(database.get_db),
):
    return db.query(models.Example).all()


@router.post("/", response_model=schemas.ExampleOut, status_code=201)
@limiter.limit("10/hour")
def create_example(
    request: Request,
    data: schemas.ExampleCreate,
    db: Session = Depends(database.get_db),
):
    obj = models.Example(name=data.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ===== YOUR ROUTERS =====
# router = APIRouter(prefix="/habits", tags=["Habits"])
# ...
