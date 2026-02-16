from pydantic import BaseModel,Field, ConfigDict
from typing import Optional
from decimal import Decimal
from src.enums import (HousingMarketEnum, StatusBuildEnum, DistrictEnum, MicroDistrictEnum,
                       BuildTypeEnum, PaymentEnum, FinishingEnum, UtilityBillsChoice)


class FilterBase(BaseModel):
    housing_market: Optional[HousingMarketEnum] = None
    build_status: Optional[StatusBuildEnum] = None
    district: Optional[DistrictEnum] = None
    microdistrict: Optional[MicroDistrictEnum] = None
    type_build: Optional[BuildTypeEnum] = None
    payment: Optional[PaymentEnum] = None
    finishing: Optional[FinishingEnum] = None
    utility_bills: Optional[UtilityBillsChoice] = None

    rooms: Optional[int] = Field(None, ge=0, description="Кількість кімнат")
    price_from: Optional[Decimal] = Field(None, ge=0)
    price_to: Optional[Decimal] = Field(None, ge=0)
    area_from: Optional[float] = Field(None, ge=0)
    area_to: Optional[float] = Field(None, ge=0)
    distance_to_the_sea: Optional[int] = Field(None, ge=0)
    ceiling_height: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = True
