#src/advert/schemas/advert/advert_base_sch.py

from pydantic import BaseModel, Field, field_validator
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

    rooms: Optional[int] = Field(
        None,
        ge=0,
        le=100,
        examples=[2]
    )
    area: Optional[Decimal] = Field(
        None,
        gt=0,
        max_digits=10,
        decimal_places=2,
        examples=[55.50]
    )
    kitchen_area: Optional[Decimal] = Field(
        None,
        gt=0,
        max_digits=10,
        decimal_places=2,
        examples=[12.00]
    )

    is_balcony: bool = False
    commission: Optional[Decimal] = Field(
        None,
        ge=0,
        max_digits=10,
        decimal_places=2,
        examples=[500.00]
    )

    price: Decimal = Field(
        ...,
        gt=0,
        max_digits=12,  # Максимум 999,999,999,9.99
        decimal_places=2,
        examples=[15000.00]
    )
    description: Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "address": "г.Киев, ул. Вайбкодера 1",
                    "appointment": "Апартаменты",
                    "price": 15000.00,
                    "area": 55.50,
                    "kitchen_area": 12.00,
                    "commission": 500.00,
                    "rooms": 2
                }
            ]
        }
    }
    # gallery: GalleryRead  | None
    @field_validator('price', 'area', 'kitchen_area', 'commission', mode='after')
    @classmethod
    def format_decimal(cls, v):
        if v is None:
            return v
        # Округлюємо до 2 знаків, щоб позбутися "хвостів" як у вашому прикладі
        return v.quantize(Decimal('0.01'))
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



