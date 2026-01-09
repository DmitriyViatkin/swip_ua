from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, Enum, \
    Numeric, Table
from sqlalchemy.orm import relationship
from src.database import Base
from src.enums import (
    AppointmentEnum, LayoutEnum, StateEnum, HeatingEnum,
    PaymentPartyEnum, CommunicationPartyEnum
)




class Advert(Base):
    __tablename__ = "adverts"

    # PK
    id = Column(Integer, primary_key=True, index=True)  # AutoField -> Integer, PK

    # Fields
    address = Column(String)  # CharField -> String

    # Enum Fields
    appointment = Column(Enum(AppointmentEnum), nullable=False)
    layout = Column(Enum(LayoutEnum))
    state = Column(Enum(StateEnum))
    heating = Column(Enum(HeatingEnum))
    payment = Column(Enum(PaymentPartyEnum))
    communication = Column(Enum(CommunicationPartyEnum))

    # Other Fields
    rooms = Column(Integer)
    area = Column(Float)
    kitchen_area = Column(Float)
    is_balcony = Column(Boolean, default=False)
    commission = Column(Float)
    description = Column(Text)
    price = Column(
        Numeric(precision=10, scale=2))
    is_approved = Column(Boolean, default=False)

    is_active = Column(Boolean, default=False)
    gallery_id = Column(Integer, ForeignKey("galleries.id"), nullable=True)
    gallery = relationship("Gallery")

    build_id = Column(Integer, ForeignKey("houses.id"), nullable=False)


    build = relationship("House", back_populates="adverts")

    promotion = relationship("Promotion", back_populates="advert", uselist=False)
