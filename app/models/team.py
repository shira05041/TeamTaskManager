from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    creator = relationship("User", backref="created_teams")
    members = relationship("TeamMembership", back_populates="team")


class TeamMembership(Base):
    __tablename__ = 'team_memberships'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), primary_key=True)    
    role = Column(String, default="member")

    user = relationship("User", backref="team_memberships")
    team = relationship("Team", back_populates="members")