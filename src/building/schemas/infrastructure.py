from pydantic import BaseModel
from src.enums import (
    BuildingStatus, BuildingType, HomeClass, ConstructionTechnology,
    TerritoryChoice, GasChoice, HeatingChoice, SewerageChoice,
    WaterSupplyChoice, UtilityBillsChoice
)


class InfrastructureBase(BaseModel):
    status: BuildingStatus | None = None
    type_build: BuildingType | None = None
    class_at_home: HomeClass | None = None
    construction_technology: ConstructionTechnology | None = None
    territory: TerritoryChoice | None = None
    gas: GasChoice | None = None
    heating: HeatingChoice | None = None
    sewerage: SewerageChoice | None = None
    water_supply: WaterSupplyChoice | None = None
    utility_bills: UtilityBillsChoice | None = None
    distance_to_sea: int | None = None
    ceiling_height: float | None = None


class InfrastructureUpdate(InfrastructureBase):
    pass


class InfrastructureRead(InfrastructureBase):
    id: int
    house_id: int

    model_config = {"from_attributes": True}