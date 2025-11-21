from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)  # путь к файлу
    uploaded_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    house_id = Column(Integer, ForeignKey("houses.id"))

    house = relationship("House", back_populates="documents")
