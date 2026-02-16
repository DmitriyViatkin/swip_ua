from src.database import Base
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from src.enums import ComplaintReasonEnum
from datetime import datetime

class Complaint(Base):
    """
        Модель для скарг на оголошення.
    """
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)

    reason = Column(Enum(ComplaintReasonEnum), nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    advert_id = Column(Integer, ForeignKey("adverts.id", ondelete="CASCADE"), nullable=False)


    author = relationship("User", back_populates="complaints")
    advert = relationship("Advert", back_populates="complaints")


    __table_args__ = (
        UniqueConstraint('user_id', 'advert_id', name='_user_advert_complaint_uc'),
    )