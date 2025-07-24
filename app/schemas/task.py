from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskStatus(str, Enum):
    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    

class TaskBase(BaseModel):
    title: constr = constr(min_length=1, max_length=100)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM
    status: Optional[TaskStatus] = TaskStatus.TO_DO

class TaskCreate(TaskBase):
    project_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None 
    status: Optional[TaskStatus] = None
    assigned_to: Optional[str] = None

class TaskOut(TaskBase):
    id: int
    project_id: int
    created_by: int
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True