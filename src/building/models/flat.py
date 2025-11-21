from sqlalchemy import (Column, Integer, DateTime, Boolean, ForeignKey,
                        DECIMAL, String, Float)
from sqlalchemy.orm import relationship
from .riser import Riser
from src.database import Base
from .floor import Floor

class Flat(Base):
    __tablename__ = "flats"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String(200))

    price = Column(DECIMAL)
    price_metr = Column(DECIMAL)
    area = Column(Float)

    floor_id = Column(Integer, ForeignKey("floors.id"))
    floor = relationship("Floor", back_populates="flats")

    riser_id = Column(Integer, ForeignKey("risers.id"))
    riser = relationship("Riser", back_populates="flats")
