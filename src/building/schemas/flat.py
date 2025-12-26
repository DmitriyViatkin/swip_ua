from pydantic import BaseModel
from decimal import Decimal


class FlatBase(BaseModel):
    image: str | None = None
    price: Decimal | None = None
    price_metr: Decimal | None = None
    area: float | None = None


class FlatCreate(FlatBase):
    floor_id: int
    riser_id: int


class FlatRead(FlatBase):
    id: int
    floor_id: int
    riser_id: int

    model_config = {"from_attributes": True}