from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey,String

from src.database import Base
from sqlalchemy.orm import relationship

class Gallery(Base):
    __tablename__ = "galleries"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String(255))
    is_main = Column(Boolean, default=False)

    house_id = Column(Integer, ForeignKey("houses.id"))
    house = relationship("House", back_populates="gallery")