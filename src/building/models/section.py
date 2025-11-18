from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from src.database import Base
from .models.corps import Corps

class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)

    corps_id = Column(Integer, ForeignKey("corps.id"))
    corps = relationship("Corps", back_populates="sections")

    floors = relationship("Floor",
                          back_populates="section", cascade="all, delete-orphan")
    risers = relationship("Riser",
                          back_populates="section", cascade="all, delete-orphan")
