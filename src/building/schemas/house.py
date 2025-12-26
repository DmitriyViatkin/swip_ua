from pydantic import BaseModel


class HouseBase(BaseModel):
    information: str | None = None
    latitude: str | None = None
    longitude: str | None = None


class HouseCreate(HouseBase):
    user_id: int


class HouseRead(HouseBase):
    id: int
    user_id: int

    model_config = {
        "from_attributes": True,
    }

class HouseUpsert(BaseModel):
    information: str| None = None
    latitude: str| None = None
    longitude: str| None = None
