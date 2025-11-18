from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, File,String
from sqlalchemy.orm import relationship

from src.database import Base
from .models.house import House

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    file_path = Column(String(255))

    house_id = Column(Integer, ForeignKey("houses.id"))
    house = relationship("House", back_populates="documents")
