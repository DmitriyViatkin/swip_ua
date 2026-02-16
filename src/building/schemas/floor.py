from pydantic import BaseModel


class FloorBase(BaseModel):
    name: int


class FloorCreate(FloorBase):
    section_id: int


class FloorRead(FloorBase):
    id: int
    section_id: int

    model_config = {"from_attributes": True}