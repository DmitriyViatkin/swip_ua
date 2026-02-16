import base64
from pydantic import BaseModel
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

    model_config = {
        "from_attributes": True
    }


    model_config = {
        "from_attributes": True,
    }

class HouseUpsert(BaseModel):
    information: str| None = None
    latitude: str| None = None
    longitude: str| None = None
    images: list[ImageWithPosition] | None = None
