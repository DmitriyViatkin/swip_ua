from src.database import Base

from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Index
)
from sqlalchemy.orm import relationship

class Gallery(Base):
    __tablename__ = "galleries"
    id = Column(Integer, primary_key=True)

    images = relationship("GalleryImage", back_populates="gallery", cascade="all, delete-orphan", order_by="GalleryImage.position")


class GalleryImage(Base):
    __tablename__ = "gallery_images"

    id = Column(Integer, primary_key=True)
    gallery_id = Column(Integer, ForeignKey("galleries.id", ondelete="CASCADE"), nullable=False)
    image = Column(String(255), nullable=False)
    position = Column(Integer, nullable=False)
    is_main = Column(Boolean, default=False, nullable=False)

    gallery = relationship("Gallery", back_populates="images")