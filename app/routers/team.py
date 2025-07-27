from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.models import User
from app.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix="/teams",
    tags=["teams"]
)

@router.get("/", response_model=List[schemas.TeamOut])
async def get_teams(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    teams = db.query(models.Team).all()
    return teams

@router.post("/", response_model=schemas.TeamOut, status_code=status.HTTP_201_CREATED)
async def create_team(
    team: schemas.TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_team = models.Team(
        name=team.name,
        created_by=current_user.id
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

@router.get("/{team_id}", response_model=schemas.TeamOut)
async def get_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.put("/{team_id}", response_model=schemas.TeamOut)
async def update_team(
    team_id: int,
    team_data: schemas.TeamUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    team = db.query(models.Team.filter(team_id == models.Team.id)).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    if team.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this team")
    
    for key, value in team_data.dict(exclude_unset=True).items():
        setattr(team, key, value)
    db.commit()
    db.refresh(team)
    return team

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if team.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this team")
    db.delete(team)
    db.commit()
    return {"detail": "Team deleted successfully"}

@router.post("/{team_id}/members", response_model=schemas.TeamMemberOut)
async def add_team_member(
    team_id: int,
    member: schemas.TeamMemberCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")   
    
    if team.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add members to this team")
    
    new_membership = models.TeamMemberShip(
        team_id = team.id,
        user_id = member.user_id
    )
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    return new_membership