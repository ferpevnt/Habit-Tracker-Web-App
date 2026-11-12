from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ===== EXAMPLE SCHEMA (delete me) =====
class ExampleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class ExampleOut(BaseModel):
    id: int
    name: str
    created_date: datetime

    model_config = {"from_attributes": True}


# ===== YOUR SCHEMAS =====
# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str = Field(..., min_length=8, max_length=56)
#
# class UserOut(BaseModel):
#     id: int
#     email: EmailStr
#     created_date: datetime
#     model_config = {"from_attributes": True}
