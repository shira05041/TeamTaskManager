from pydantic import BaseModel
from typing import Optional, List

class ProjectBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    members: List[str] = []

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    members: Optional[List[str]] = None

class ProjectOut(ProjectBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True