from sqlalchemy import Column, Integer, Text, ForeignKey, String, DECIMAL, Boolean
from sqlalchemy.orm import relationship

from src.database import Base
from .models.house import House


class Advantages_of_Home(Base):
    __tablename__ = "advantages_of_home"

    id = Column(Integer, primary_key=True, index=True)
    is_parking = Column(Boolean, default=True)
    is_sports_ground = Column(Boolean, default=True)

    house_id = Column(Integer, ForeignKey("houses.id"))
    house = relationship("House", back_populates="advantages_of_home")