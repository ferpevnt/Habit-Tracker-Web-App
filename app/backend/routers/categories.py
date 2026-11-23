from fastapi import APIRouter, Depends, Request, HTTPException, status, Response
from sqlalchemy.orm import Session
from database import database, models, schemas
from security.limiter import limiter
from security.security import get_current_user
from config.config import settings
from typing import List

router = APIRouter(prefix="/categories", tags=["Categories"])

def find_category(user_id: int, category_id: int, db) -> models.Category:
    category = db.query(
            models.Category
        ).filter(
            models.Category.user_id == user_id,
            models.Category.id == category_id
        ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category
def category_name_unique(user_id: int, category_name: str, db, exclude_id=None) -> models.Category:
    category = db.query(
            models.Category
        ).filter(
            models.Category.name == category_name,
            models.Category.user_id == user_id
        )
    if exclude_id is not None:
        category = category.filter(
            models.Category.id != exclude_id
        )
    category = category.first()
    if category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with such name already exists"
            )

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.CategoryGet])
@limiter.limit("30/minute")
@limiter.limit("300/hour")
def CategoriesGet(
    request: Request,
    user: models.User=Depends(get_current_user),
    db: Session=Depends(database.get_db)):

    categories = db.query(
        models.Category.id,
        models.Category.name,
        models.Category.emoji,
        models.Category.color,
        models.Category.created_at
    ).filter(
        models.Category.user_id == user.id
    ).all()

    return categories

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.CategoryGet)
@limiter.limit("60/minute")
def CategoryGet(
    request: Request,
    id: int,
    user: models.User=Depends(get_current_user),
    db: Session=Depends(database.get_db)):

    category = find_category(user.id, id, db)
    return category

@router.get("/{id}/habits", status_code=status.HTTP_200_OK, response_model=schemas.CategoryWithHabits)
@limiter.limit("30/minute")
def HabitsGetCategory(
    request: Request,
    id: int,
    user: models.User=Depends(get_current_user),
    db: Session=Depends(database.get_db)):

    category = find_category(user.id, id, db)
    category_habits = db.query(
        models.Habit.id,
        models.Habit.title,
        models.Habit.emoji,
        models.Habit.created_at,
        models.Habit.archived_at
    ).filter(
        models.Habit.category_id == id,
        models.Habit.user_id == user.id
    ).all()
    return {
    "id": category.id,
    "name": category.name,
    "emoji": category.emoji,
    "color": category.color,
    "created_at": category.created_at,
    "habits": category_habits,
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
@limiter.limit("20/hour")
@limiter.limit("40/day")
def CategoryCreate(
    category: schemas.CategoryCreate,
    request: Request,
    user: models.User=Depends(get_current_user),
    db: Session=Depends(database.get_db)):

    existing_category = category_name_unique(user.id, category.name, db)
    
    new_category = models.Category(
        user_id = user.id,
        name = category.name,
        emoji = category.emoji,
        color = category.color)
    
    db.add(new_category)
    db.commit()
    return 

@router.put("/{id}", status_code=status.HTTP_200_OK)
@limiter.limit("30/hour")
def CategoryUpdate(
    id: int,
    category: schemas.CategoryUpdate,
    request: Request,
    user: models.User=Depends(get_current_user),
    db: Session=Depends(database.get_db)):

    if category.name:
        existing_category = category_name_unique(user.id, category.name, db, id)
    category_db = find_category(user.id, id, db)

    if category.name is not None:
        category_db.name = category.name
    if category.emoji is not None:
        category_db.emoji = category.emoji
    if category.color is not None:
        category_db.color = category.color

    db.commit()
    return 
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
@limiter.limit("30/hour")
def CategoryDelete(
    id: int,
    request: Request,
    user: models.User=Depends(get_current_user),
    db: Session=Depends(database.get_db)):

    category = find_category(user.id, id, db)
    db.delete(category)
    db.commit()
    return



        
    


