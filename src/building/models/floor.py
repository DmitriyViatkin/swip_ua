from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base
from .models.section import Section


class Floor(Base):
    __tablename__ = "floors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer, index=True)

    section_id = Column(Integer, ForeignKey("sections.id"))
    section = relationship("Section", back_populates="floors")

    flats = relationship("Flat", back_populates="floor",
                         cascade="all, delete-orphan")
