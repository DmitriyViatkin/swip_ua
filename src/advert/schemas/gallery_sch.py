# gallery_sch.py
from pydantic import BaseModel
from typing import List
from ..schemas.gallery_image_sch import GalleryImageRead



class GalleryRead(BaseModel):
    id: int
    images: List[GalleryImageRead] = []

    model_config = {
        "from_attributes": True
    }