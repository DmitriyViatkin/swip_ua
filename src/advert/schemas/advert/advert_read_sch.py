#src/advert/schemas/advert/advert_read_sch.py

from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional
from ..gallery_image_sch import GalleryImageRead
from .. gallery_sch import GalleryRead
from ..promotion.promotion_read_sch import PromotionRead
from src.enums import (
    AppointmentEnum, LayoutEnum, StateEnum, HeatingEnum,
    PaymentPartyEnum, CommunicationPartyEnum
)

class AdvertRead(BaseModel):
    id: int
    address: str

    appointment: AppointmentEnum
    layout: Optional[LayoutEnum]
    state: Optional[StateEnum]
    heating: Optional[HeatingEnum]
    payment: Optional[PaymentPartyEnum]
    communication: Optional[CommunicationPartyEnum]

    rooms: Optional[int]
    area: Optional[Decimal]
    kitchen_area: Optional[Decimal]
    is_balcony: bool
    commission: Optional[Decimal]
    description: Optional[str]
    price: Decimal
    gallery: GalleryRead | None
    build_id: int
    promotion: Optional[PromotionRead]
    is_approved: bool
    is_active: bool

    
    model_config = ConfigDict(from_attributes=True)