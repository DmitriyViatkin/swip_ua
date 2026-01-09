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

    @classmethod
    def as_form(
        cls,
        address: Optional[str] = Form(None),
        appointment: Optional[AppointmentEnum] = Form(None),
        price: Optional[Decimal] = Form(None),

        layout: Optional[LayoutEnum] = Form(None),
        state: Optional[StateEnum] = Form(None),
        heating: Optional[HeatingEnum] = Form(None),
        payment: Optional[PaymentPartyEnum] = Form(None),
        communication: Optional[CommunicationPartyEnum] = Form(None),
        rooms: Optional[int] = Form(None),
        area: Optional[Decimal] = Form(None),
        kitchen_area: Optional[Decimal] = Form(None),
        is_balcony: Optional[bool] = Form(None),
        commission: Optional[Decimal] = Form(None),
        description: Optional[str] = Form(None),
    ):
        return cls(
            address=address,
            appointment=appointment,
            price=price,
            layout=layout,
            state=state,
            heating=heating,
            payment=payment,
            communication=communication,
            rooms=rooms,
            area=area,
            kitchen_area=kitchen_area,
            is_balcony=is_balcony,
            commission=commission,
            description=description,
        )