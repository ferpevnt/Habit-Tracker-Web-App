from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator
from typing import Optional, List
from datetime import datetime
import re

# ===== AUTH =====
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=40, description="User's name (3-40 characters)")
    email: EmailStr = Field(..., description="User's email")
    password: str = Field(..., min_length=8, max_length=56, description="User's password (8-56 chars, must include uppercase, lowercase, digit, special)")
    confirm_password: str = Field(..., min_length=8, max_length=56, description="User's confirm password (must match password)")

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must have at least one capital letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must have at least one lower letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must have at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must have at least one special symbol")
        return value

    @model_validator(mode="after")
    def validate_password_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords don't match")  
        return self

class UserLogin(BaseModel):
    email : EmailStr
    password: str = Field(..., min_length=8, max_length=56)

class UserOut(BaseModel):
    name: str
    email: EmailStr
    is_verified: bool
    timezone: str
    created_at: datetime
    
    model_config = {"from_attributes": True}

# ===== CATEGORIES =====
class CategoryGet(BaseModel):
    id: int
    name: str
    emoji: str
    color: str
    created_at: datetime

class HabitShort(BaseModel):
    id: int
    title: str
    emoji: Optional[str]
    created_at: datetime
    archived_at: Optional[datetime]
    model_config = {"from_attributes": True}
    
class CategoryWithHabits(BaseModel):
    id: int
    name: str
    emoji: str
    color: str
    created_at: datetime
    habits: List[HabitShort]

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=40, description="Category name (3-40 characters)")
    emoji: Optional[str] = Field(None, max_length=20, description="Category emoji (<= 20 characters)")
    color: str = Field(..., pattern=r"^#[0-9a-fA-F]{6}$", description="Category color ")

    @field_validator("name", mode="after")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.capitalize().strip()

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=40, description="Category name (3-20 characters)")
    emoji: Optional[str] = Field(None, max_length=20, description="Category emoji (<= 20 characters)")
    color: Optional[str] = Field(None, pattern=r"^#[0-9a-fA-F]{6}$", description="Category color")
    @field_validator("name", mode="after")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        if value is None:
            return value
        return value.capitalize().strip()
    
    @model_validator(mode="after")
    def null_request_check(self):
        if all(value is None for value in self.model_dump(exclude_unset=True).values()):
            raise ValueError("At least one field must be provided")
