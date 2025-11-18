from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base
from src.enums import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    phone = Column(String(20), index=True)
    email = Column(String(100), unique=True, index=True)
    role = Column(Enum(UserRole), default=UserRole.CLIENT)
    date = Column(DateTime, server_default=func.now())

    client_notifications = relationship(
        "Notification",
        back_populates="client",
        foreign_keys="[Notification.client_id]"
    )

    agent_notifications = relationship(
        "Notification",
        back_populates="agent",
        foreign_keys="[Notification.agent_id]"
    )

    black_list = relationship(
        "BlackList",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    filters = relationship(
        "Filter",
        back_populates="user",
        cascade="all, delete-orphan"
        )
