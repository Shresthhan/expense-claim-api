"""User schemas."""
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    role: UserRole
    manager_id: Optional[int] = None

    class Config:
        from_attributes = True