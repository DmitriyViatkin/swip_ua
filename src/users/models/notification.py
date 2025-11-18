from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base
from .models.users import User

class Notification (Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(Integer, ForeignKey("users.id"))
    agent_id = Column(Integer, ForeignKey("users.id"))

    client = relationship(
        "User",
        foreign_keys=[client_id],
        back_populates="client_notifications"
    )

    agent = relationship(
        "User",
        foreign_keys=[agent_id],
        back_populates="agent_notifications"
    )

    is_me = Column(Boolean, default=False)
    is_me_agent = Column(Boolean, default=False)
    is_agent = Column(Boolean, default=False)
    turn_off  = Column(Boolean, default=False)