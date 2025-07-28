from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import project as models
from app.schemas import project as schemas
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix='/projects', tags=["projects"])

@router.get("/", response_model=List[schemas.ProjectOut])
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    projects = db.query(models.Project).join(models.Team).join(models.Team.members).filter((models.Project.owner_id == current_user.id) | (models.Team.members.any(id=current_user.id))).all()
    return projects

@router.post("/", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_project = models.Project(**project.dict(), owner_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id and current_user.id not in project.team.members:
        raise HTTPException(status_code=403, detail="Not authorized to access this project")
    return project

@router.patch("/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, update_data: schemas.ProjectUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != current_user.id and current_user.id not in project.team.members:
        raise HTTPException(status_code=403, detail="Not authorized to update this project")
    
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != current_user.id and current_user.id not in project.team.members:
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")
    
    db.delete(project)
    db.commit()
    return {"detail": "Project deleted successfully"}