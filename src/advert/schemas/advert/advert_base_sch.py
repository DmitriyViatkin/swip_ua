#src/advert/schemas/advert/advert_base_sch.py

from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from src.enums import (
                AppointmentEnum,LayoutEnum,StateEnum,HeatingEnum,
                PaymentPartyEnum,CommunicationPartyEnum
)

class AdvertBase(BaseModel):
    address: str = Field(..., examples=["г.Киев, ул. Вайбкодера 1"])

    appointment: AppointmentEnum
    layout: Optional[LayoutEnum] = None
    state: Optional[StateEnum] = None
    heating: Optional[HeatingEnum] =None
    payment: Optional[PaymentPartyEnum]=None
    communication: Optional[CommunicationPartyEnum]=None

    rooms: Optional[int] = Field(None, ge=0)
    area: Optional[Decimal] = Field(None,gt=0)
    kitchen_area: Optional[Decimal] = Field(None, gt=0)

    is_balcony: bool = False
    commission: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = None
    price: Decimal = Field(...,gt=0)



