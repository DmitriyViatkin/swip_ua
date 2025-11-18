from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base

from listings.models import Gallery


class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    information = Column(Text)
    latitude = Column(String(50))
    longitude = Column(String(50))

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="houses")

    gallery_id = Column(Integer, ForeignKey("galleries.id"))
    gallery = relationship("Gallery", back_populates="house")

    corps = relationship("Corps", back_populates="house", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="house", cascade="all, delete-orphan")
    news = relationship("News", back_populates="house", cascade="all, delete-orphan")

    registration_and_payment = relationship(
        "Registration_and_Payment", back_populates="house", uselist=False
    )
    advantages_of_home = relationship(
        "Advantages_of_Home", back_populates="house", uselist=False
    )
    infrastructure = relationship(
        "Infrastructure", back_populates="house", uselist=False
    )