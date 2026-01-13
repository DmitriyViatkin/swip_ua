#src/advert/schemas/advert/advert_update_sch.py

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from fastapi import Form
from src.enums import (
                AppointmentEnum,LayoutEnum,StateEnum,HeatingEnum,
                PaymentPartyEnum,CommunicationPartyEnum
)

class AdvertUpdate(BaseModel):

    address: Optional[str]=None

    appointment: Optional[AppointmentEnum] = None
    layout: Optional[LayoutEnum] = None
    state: Optional[StateEnum] = None
    heating: Optional[HeatingEnum] = None
    payment: Optional[PaymentPartyEnum] = None
    communication: Optional[CommunicationPartyEnum] = None

    rooms: Optional[int] = None
    area: Optional[Decimal] = None
    kitchen_area: Optional[Decimal] = None
    is_balcony: Optional[bool] = None
    commission: Optional[Decimal] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None

