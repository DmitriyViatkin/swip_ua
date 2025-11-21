from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base
from .users import User

class Redirections (Base):
    __tablename__ = "redirections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), )
    user = relationship("User", back_populates = "redirections")
    date = Column(DateTime, server_default=func.now())
