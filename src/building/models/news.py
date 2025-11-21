from sqlalchemy import Column, Integer, Text, ForeignKey, String
from sqlalchemy.orm import relationship

from src.database import Base
from .house import (House)

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)

    house_id = Column(Integer, ForeignKey("houses.id"))
    house = relationship("House", back_populates="news")