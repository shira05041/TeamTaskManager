from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class UserLogin(BaseModel):
    username: str
    password: str

class UserLogOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True