from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Text, Enum, func
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from src.database import Base
from .advert import Advert
from src.enums import TypeEnum


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    add_frase = Column(Text)
    is_color = Column(Boolean, default=False)
    is_big_advert = Column(Boolean, default=False)
    type_promotion = Column(Enum(TypeEnum))

    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)

    advert_id = Column(Integer, ForeignKey("adverts.id"))
    advert = relationship("Advert", back_populates="promotion")

    @property
    def is_active(self) -> bool:
        now = datetime.now(timezone.utc)

        if self.end_date is None:
            return self.start_date <= now

        return self.start_date <= now <= self.end_date
