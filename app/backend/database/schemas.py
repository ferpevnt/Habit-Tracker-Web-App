from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator
from typing import Optional
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
    