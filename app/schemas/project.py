from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class ProjectBase(BaseModel):
    name: constr = constr(min_length=1, max_length=100)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    team_id: int

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    team_id: Optional[int] = None

class ProjectOut(ProjectBase):
    id: int
    team_id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True