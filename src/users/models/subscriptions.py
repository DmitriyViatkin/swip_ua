from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base
from .models.users import User

class Subscription (Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), )
    user = relationship("User", back_populates = "subscription")
    date = Column(DateTime, server_default=func.now())
    auto_renewal = Column(Boolean, default=True)