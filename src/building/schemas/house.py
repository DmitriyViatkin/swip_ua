import base64
from pydantic import BaseModel, ConfigDict
from .infrastructure import InfrastructureRead
from .news import NewsRead
from .registration_and_payment import RegistrationPaymentRead
from ...users.schemas.user.user_read import UserAgentRead
from src.advert.schemas.image_sch import ImageWithPosition
from src.advert.schemas.gallery_image_sch import GalleryImageRead
from src.advert.schemas.gallery_sch import GalleryRead
from .document import DocumentRead

from typing import Optional, List


class HouseBase(BaseModel):
    information: str | None = None
    latitude: str | None = None
    longitude: str | None = None


class HouseCreate(HouseBase):
    user_id: int
    images: list[ImageWithPosition] | None = None


class HouseRead(HouseBase):
    id: int
    user_id: int

    infrastructure: Optional[InfrastructureRead] = None
    registration_and_payment: Optional[RegistrationPaymentRead] = None
    sales_department: Optional[UserAgentRead] = None
    news: Optional[List[NewsRead]] = None
    documents: Optional[List[DocumentRead]] = None
    add_excell: Optional[List[DocumentRead]] = None

    gallery: Optional[GalleryRead] = None


    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 10,
                "information": "ЖК 'Сучасний', преміум клас",
                "latitude": "50.4501",
                "longitude": "30.5234",
                "infrastructure": None,
                "registration_and_payment": None,
                "sales_department": None,
                "news": [],
                "documents": [],
                "add_excell": [],
                "gallery": {
                    "id": 1,
                    "images": [
                        {"id": 1, "url": "http://example.com/img.jpg", "position": 1}
                    ]
                }
            }
        }
    )


class HouseUpsert(BaseModel):
    information: str | None = None
    latitude: str | None = None
    longitude: str | None = None
    images: list[ImageWithPosition] | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "information": "Оновлена інформація про будинок",
                "latitude": "50.4501",
                "longitude": "30.5234",
                "images": [
                    {"image_id": 0, "base64": "string", "position": 0, "is_delete": False}
                ]
            }
        }
    )