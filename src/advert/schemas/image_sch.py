from typing import Optional, List
from pydantic import BaseModel, Field
from src.advert.schemas.advert.advert_update_sch import AdvertUpdate
from src.advert.schemas.galery_order import GalleryOrder
from src.advert.schemas.advert.advert_create_sch import AdvertCreate

class ImageWithPosition(BaseModel):
    """Схема для загрузки картинки с указанием её позиции"""
    image_id: Optional[int] = Field(
        None, description="ID існуючого зображення"
    )
    base64: Optional[str] = Field(
        None, description="Base64 нового зображення"
    )
    position: Optional[int] = Field(
        None, description="Нова позиція зображення"
    )
    is_delete: bool = Field(
        False, description="Позначка для видалення"
    )

class AdvertUpdateWithImages(AdvertUpdate):
    """Расширенная схема обновления объявления с изображениями"""

    images: Optional[List[ImageWithPosition]] = None

class ImageWithPosition(BaseModel):
    image_id: Optional[int] = None
    base64: Optional[str] = None
    position: Optional[int] = None
    is_delete: bool = False

class AdvertCreateWithImages(AdvertCreate):
    images: Optional[List[ImageWithPosition]] = None