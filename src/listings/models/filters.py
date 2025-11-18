from sqlalchemy import Column, Integer, String, Float, Numeric, Boolean, ForeignKey, \
    Enum
from sqlalchemy.orm import relationship
from src.database import Base

from  src.enums import (
    HousingMarketEnum,
    BuildStatusEnum,
    DistrictEnum,
    MicroDistrictEnum,
    BuildTypeEnum,
    PaymentEnum,
    FinishingEnum,
    UtilityBillsEnum
)


class Filter(Base):
    """
    Модель для хранения пользовательских фильтров поиска недвижимости.
    """
    __tablename__ = "filters"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", back_populates="filters")

    housing_market = Column(Enum(HousingMarketEnum, name="housing_market_enum"),
                            nullable=True)
    build_status = Column(Enum(BuildStatusEnum, name="build_status_enum"),
                          nullable=True)
    district = Column(Enum(DistrictEnum, name="district_enum"), nullable=True)
    microdistrict = Column(Enum(MicroDistrictEnum, name="microdistrict_enum"),
                           nullable=True)
    type_build = Column(Enum(BuildTypeEnum, name="build_type_enum"), nullable=True)
    payment = Column(Enum(PaymentEnum, name="payment_enum"), nullable=True)
    finishing = Column(Enum(FinishingEnum, name="finishing_enum"), nullable=True)
    utility_bills = Column(Enum(UtilityBillsEnum, name="utility_bills_enum"),
                           nullable=True)
    rooms = Column(Integer, nullable=True)
    price_from = Column(Numeric(12, 2), nullable=True)
    price_to = Column(Numeric(12, 2), nullable=True)
    area_from = Column(Float, nullable=True)
    area_to = Column(Float, nullable=True)
    distance_to_the_sea = Column(Integer, nullable=True)
    ceiling_height = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", back_populates="filters")