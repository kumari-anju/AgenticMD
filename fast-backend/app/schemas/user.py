from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Optional[str] = None
    organization: Optional[str] = None

class UserCreate(UserBase):
    password: str
    confirm_pass: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
