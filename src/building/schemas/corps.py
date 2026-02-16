from pydantic import BaseModel


class CorpsBase(BaseModel):
    name: str


class CorpsCreate(CorpsBase):
    house_id: int


class CorpsRead(CorpsBase):
    id: int
    house_id: int

    model_config = {"from_attributes": True}