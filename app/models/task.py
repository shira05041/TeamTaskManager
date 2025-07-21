from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum

class TaskStatus(str, PyEnum):
    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String(500))
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    assigned_to = Column(Integer, ForeignKey('users.id'), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TO_DO)
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", backref="assigned_tasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
