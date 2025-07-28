from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime


class CommentBase(BaseModel):
    content: constr = constr(min_length=1, max_length=500)
    task_id: int

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: str

class CommentOut(CommentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True