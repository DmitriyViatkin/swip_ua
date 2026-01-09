from pydantic import BaseModel
from typing import List


class GalleryOrder(BaseModel):
    image_id: int
    position: int
    is_main: bool = False