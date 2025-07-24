from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import date


class UserBase(BaseModel):
    username: constr = constr(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(BaseModel):
    password: constr = constr(min_length=8)  

class UserUpdate(BaseModel):
    username = Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[constr] = None

class UserOut(BaseModel):
    id: int
    created_at: str
    is_active: bool = True

    class Config:
        from_attributes = True