from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey,String

from src.database import Base


class Gallery (Base):
    __tablename__ = "galleries"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String(255))

    is_main = Column(Boolean, default=False)