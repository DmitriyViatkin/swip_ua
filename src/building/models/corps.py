from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, String


from sqlalchemy.orm import relationship

from src.database import Base
from .house import House

class Corps(Base):
    __tablename__ = "corps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)

    house_id = Column(Integer, ForeignKey("houses.id"))
    house = relationship("House", back_populates="corps")

    sections = relationship("Section", back_populates="corps", cascade="all, delete-orphan")