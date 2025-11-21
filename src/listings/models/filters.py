from sqlalchemy import Column, Integer, Float, Numeric, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.database import Base

# Импортируем ТОЧНЫЕ имена классов из enums.py
from src.enums import (
    HousingMarketEnum,
    StatusBuildEnum,  # Исправленный класс (стадии стройки)
    DistrictEnum,
    MicroDistrictEnum,
    BuildTypeEnum,  # Исправленный класс (тип здания)
    PaymentEnum,  # Добавленный класс
    FinishingEnum,
    UtilityBillsChoice  # В enums.py он называется Choice, а не Enum
)


class Filter(Base):
    """
    Модель для хранения пользовательских фильтров поиска недвижимости.
    """
    __tablename__ = "filters"

    id = Column(Integer, primary_key=True, index=True)

    # --- Связь с User (Один раз!) ---
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", back_populates="filters")

    # --- Поля фильтров (Enums) ---
    housing_market = Column(Enum(HousingMarketEnum, name="housing_market_enum"),
                            nullable=True)

    # Используем исправленный StatusBuildEnum (Сдан/Котлован)
    build_status = Column(Enum(StatusBuildEnum, name="build_status_enum"),
                          nullable=True)

    district = Column(Enum(DistrictEnum, name="district_enum"),
                      nullable=True)

    microdistrict = Column(Enum(MicroDistrictEnum, name="microdistrict_enum"),
                           nullable=True)

    # Используем исправленный BuildTypeEnum (Квартирный дом/Частный дом)
    type_build = Column(Enum(BuildTypeEnum, name="build_type_enum"),
                        nullable=True)

    # Используем добавленный PaymentEnum
    payment = Column(Enum(PaymentEnum, name="payment_enum"),
                     nullable=True)

    finishing = Column(Enum(FinishingEnum, name="finishing_enum"),
                       nullable=True)

    # Используем UtilityBillsChoice (как он назван в файле enums)
    utility_bills = Column(Enum(UtilityBillsChoice, name="utility_bills_enum"),
                           nullable=True)

    # --- Числовые диапазоны ---
    rooms = Column(Integer, nullable=True)

    # Numeric(12, 2) идеально для денег
    price_from = Column(Numeric(12, 2), nullable=True)
    price_to = Column(Numeric(12, 2), nullable=True)

    area_from = Column(Float, nullable=True)
    area_to = Column(Float, nullable=True)

    distance_to_the_sea = Column(Integer, nullable=True)
    ceiling_height = Column(Float, nullable=True)

    is_active = Column(Boolean, default=True)