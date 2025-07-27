from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.models import User
from app.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get("/", response_model=List[schemas.TaskOut])
async def get_tasks(
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # start with base query
    query = db.query(models.Task)

    # apply filters
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    if status:
        query = query.filter(models.Task.status == status)

    #filter for tasks user has access to
    tasks = query.join(models.Project)\
        .join(models.Team)\
        .join(models.TeamMembership)\
        .filter(models.TeamMembership.user_id == current_user.id)\
        .all()
    
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for the given criteria")
    
    return tasks

@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(models.Project).filter(models.Task.project_id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    team_member = db.query(models.TeamMembership).filter(
        models.TeamMembership.team_id == project.team_id,
        models.TeamMembership.user_id == current_user.id
    ).first()

    if not team_member:
        raise HTTPException(status_code=403, detail="Not authorized to create task for this project")
    if team_member.role not in ["admin", "member"]:
        raise HTTPException(status_code=403, detail="Not authorized to create task for this project")
    
    new_task = models.Task(**task.dict(), created_by=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/{task_id}", response_model=schemas.TaskOut)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    team_member = db.query(models.TeamMembership).filter(
        models.TeamMembership.team_id == task.project_id.team_id,
        models.TeamMembership.user_id == current_user.id
    ).first()

    if not team_member:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    return task

@router.patch("/{task_id}", response_model=schemas.TaskOut)
async def update_task(
    task_id: int,
    update_data: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user.id not in [task.created_by, task.assigned_to]:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if current_user.id != task.created_by:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}