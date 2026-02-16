from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    description: str


class NewsCreate(NewsBase):
    house_id: int

class NewsUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class NewsRead(NewsBase):
    id: int
    house_id: int

    model_config = {"from_attributes": True}