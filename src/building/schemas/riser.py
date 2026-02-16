from pydantic import BaseModel


class RiserBase(BaseModel):
    name: int


class RiserCreate(RiserBase):
    section_id: int


class RiserRead(RiserBase):
    id: int
    section_id: int

    model_config = {"from_attributes": True}