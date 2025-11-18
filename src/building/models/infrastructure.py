from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base
from src.core.infrastructure_enums import (
    BuildingStatus, BuildingType, HomeClass, ConstructionTechnology,
    TerritoryChoice, GasChoice, HeatingChoice, SewerageChoice,
    WaterSupplyChoice, UtilityBillsChoice
)


class Infrastructure(Base):
    __tablename__ = "infrastructure"

    id = Column(Integer, primary_key=True, index=True)

    house_id = Column(Integer, ForeignKey("houses.id"))
    house = relationship("House", back_populates="infrastructure")

    status = Column(Enum(BuildingStatus, native_enum=False))
    type_build = Column(Enum(BuildingType, native_enum=False))
    class_at_home = Column(Enum(HomeClass, native_enum=False))
    construction_technology = Column(Enum(ConstructionTechnology, native_enum=False))
    territory = Column(Enum(TerritoryChoice, native_enum=False))
    gas = Column(Enum(GasChoice, native_enum=False))
    heating = Column(Enum(HeatingChoice, native_enum=False))
    sewerage = Column(Enum(SewerageChoice, native_enum=False))
    water_supply = Column(Enum(WaterSupplyChoice, native_enum=False))
    utility_bills = Column(Enum(UtilityBillsChoice, native_enum=False))

    distance_to_sea = Column(Integer)
    ceiling_height = Column(Float)
