from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.models import User
from app.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)

@router.get("/", response_model=List[schemas.CommentOut])
async def get_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    comments = db.query(models.Comment).filter(models.Comment.task_id == task_id).all() 
    return comments

@router.post("/", response_model=schemas.CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: schemas.CommentCreate,
    task_id : int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_comment = models.Comment(
        content=comment.content,
        task_id = task_id,
        user_id = current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

router.delete("/{comment_id}", response_model=schemas.CommentOut, status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
        comment_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if current_user.id != comment.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted successfully"}