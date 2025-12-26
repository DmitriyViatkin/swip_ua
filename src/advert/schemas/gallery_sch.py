# gallery_sch.py
from pydantic import BaseModel
from typing import List

class GalleryImageRead(BaseModel):
    id: int
    image: str
    position: int
    is_main: bool

    model_config = {
        "from_attributes": True
    }

class GalleryRead(BaseModel):
    id: int
    images: List[GalleryImageRead] = []

    model_config = {
        "from_attributes": True
    }