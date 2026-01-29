from src.database import Base
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from src.enums import ComplaintReasonEnum
from datetime import datetime

class Favorite (Base):

    """ Модель для "Списку бажаного" (Wishlist)."""

    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    advert_id = Column(Integer, ForeignKey("adverts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__=(
        UniqueConstraint('user_id', 'advert_id', name='_user_favorite_advert_uc'),
        )
    user = relationship("User", back_populates="favorites")
    advert= relationship("Advert")