from sqlalchemy import Column, Integer, Text, ForeignKey, String, DECIMAL
from sqlalchemy.orm import relationship

from src.database import Base
from .models.house import House

class Registration_and_Payment(Base):
    __tablename__ = "registrations_and_payments"

    id = Column(Integer, primary_key=True, index=True)

    registration = Column(Text)
    options = Column(Text)
    appointment = Column(Text)
    price = Column(DECIMAL(10, 2))

    house_id = Column(Integer, ForeignKey("houses.id"))
    house = relationship("House", back_populates="registration_and_payment")
