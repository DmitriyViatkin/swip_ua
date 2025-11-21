from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base
from  .section import Section

class Riser(Base):
    __tablename__ = "risers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer, index=True)

    section_id = Column(Integer, ForeignKey("sections.id"))
    section = relationship("Section", back_populates="risers")

    flats = relationship("Flat", back_populates="riser")
