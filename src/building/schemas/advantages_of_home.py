from pydantic import BaseModel


class AdvantagesOfHomeBase(BaseModel):
    is_parking: bool | None = True
    is_sports_ground: bool | None = True


class AdvantagesOfHomeCreate(AdvantagesOfHomeBase):
    house_id: int


class AdvantagesOfHomeRead(AdvantagesOfHomeBase):
    id: int
    house_id: int

    model_config = {"from_attributes": True}