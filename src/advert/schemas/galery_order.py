from pydantic import BaseModel

class GalleryOrder(BaseModel):

    id: int
    position: int