from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    # Кто отправил и кто получил
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    text = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    is_read = Column(Boolean, default=False)

    # Отношения
    sender = relationship("User", foreign_keys="Message.sender_id", back_populates="sent_messages")
    recipient = relationship("User", foreign_keys="Message.recipient_id", back_populates="received_messages")