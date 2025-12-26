from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base
from src.enums import UserRole
from src.advert.models.filters import Filter

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    phone = Column(String(20), index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True)
    role = Column(Enum(UserRole), default=UserRole.CLIENT)
    date = Column(DateTime, server_default=func.now())
    photo = Column(String(255), nullable=True)

    houses = relationship("House", back_populates="user", cascade="all, delete-orphan")
    client_notifications = relationship("Notification", back_populates="client", foreign_keys="[Notification.client_id]")
    agent_notifications = relationship("Notification", back_populates="agent", foreign_keys="[Notification.agent_id]")
    black_list = relationship("BlackList", back_populates="user", cascade="all, delete-orphan")
    filters = relationship("Filter", back_populates="user", cascade="all, delete-orphan")
    redirections = relationship("Redirections", back_populates="user", cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="user", cascade="all, delete-orphan", uselist=False)


    agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    agent = relationship(
        "User",
        remote_side=[id],
        back_populates="clients"
    )
    clients = relationship(
        "User",
        back_populates="agent",
        cascade="all, delete-orphan"
    )
