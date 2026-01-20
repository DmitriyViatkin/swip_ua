from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship

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

    advert_id = Column(Integer, ForeignKey("adverts.id"))
    advert = relationship("Advert", back_populates="promotion")
