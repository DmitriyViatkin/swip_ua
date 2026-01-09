#src/advert/schemas/advert/advert_create_sch.py
from pydantic import Field
from .advert_base_sch import AdvertBase
from fastapi import Form
from decimal import Decimal
from typing import Optional, List
from src.enums import (
                AppointmentEnum,LayoutEnum,StateEnum,HeatingEnum,
                PaymentPartyEnum,CommunicationPartyEnum
)
class AdvertCreate(AdvertBase):

    build_id: int = Field(..., gt=0)

    @classmethod
    def as_form(
            cls,
            address: str = Form(...),
            appointment: AppointmentEnum = Form(...),
            price: Decimal = Form(...),
            build_id: int = Form(...),

            layout: Optional[LayoutEnum] = Form(None),
            state: Optional[StateEnum] = Form(None),
            heating: Optional[HeatingEnum] = Form(None),
            payment: Optional[PaymentPartyEnum] = Form(None),
            communication: Optional[CommunicationPartyEnum] = Form(None),
            rooms: Optional[int] = Form(None),
            area: Optional[Decimal] = Form(None),
            kitchen_area: Optional[Decimal] = Form(None),
            is_balcony: bool = Form(False),
            commission: Optional[Decimal] = Form(None),
            description: Optional[str] = Form(None),
    ):
        return cls(
            address=address,
            appointment=appointment,
            price=price,
            build_id=build_id,
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


