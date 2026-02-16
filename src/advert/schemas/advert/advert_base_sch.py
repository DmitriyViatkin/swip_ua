#src/advert/schemas/advert/advert_base_sch.py

from pydantic import BaseModel, Field
from fastapi import Form
from decimal import Decimal
from typing import Optional, List
from src.enums import (
                AppointmentEnum,LayoutEnum,StateEnum,HeatingEnum,
                PaymentPartyEnum,CommunicationPartyEnum
)
from src.advert.schemas.gallery_image_sch import GalleryImageRead
from .. gallery_sch import GalleryRead
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
    # gallery: GalleryRead  | None

    @classmethod
    def as_form(
            cls,
            address: str = Form(...),
            appointment: AppointmentEnum = Form(...),
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
            price: Decimal = Form(...),
            build_id: int = Form(...),
    ):
        return cls(**locals())



