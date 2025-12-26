from pydantic import BaseModel


class SectionBase(BaseModel):
    name: str


class SectionCreate(SectionBase):
    corps_id: int


class SectionRead(SectionBase):
    id: int
    corps_id: int

    model_config = {"from_attributes": True}