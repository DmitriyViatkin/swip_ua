from pydantic import BaseModel

class GalleryImageRead(BaseModel):
    id: int
    image: str
    position: int
    is_main: bool

    model_config = {
        "from_attributes": True
    }