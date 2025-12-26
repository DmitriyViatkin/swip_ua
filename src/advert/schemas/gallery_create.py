from pydantic import BaseModel


class GalleryCreate(BaseModel):
    filename: str
    position: int
    is_main: bool = False