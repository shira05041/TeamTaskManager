from datetime import datetime
from pydantic import BaseModel, constr
from typing import List, Optional

class TeamMemberShipBase(BaseModel):
    role: Optional[str] = None

class TeamMemberShipCreate(TeamMemberShipBase):
    user_id: int
    team_id: int

class TeamMemberShipUpdate(BaseModel):
    role: Optional[str] = None
    team_id: Optional[int] = None    

class TeamMemberShipOut(TeamMemberShipBase):
    id: int
    team_id: int
    
    class Config:
        orm_mode = True   


class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    members: Optional[List[int]] = None

class TeamOut(TeamBase):
    id: int
    created_by: int
    created_at: datetime
    members: List[TeamMemberShipOut] = []
    
    class Config:
        orm_mode = True   