from pydantic import BaseModel
from datetime import datetime


class DocumentBase(BaseModel):
    file_path: str
    uploaded_at: datetime | None = None
    is_active: bool = True


class DocumentCreate(DocumentBase):
    house_id: int


class DocumentRead(DocumentBase):
    id: int
    house_id: int

    model_config = {"from_attributes": True}