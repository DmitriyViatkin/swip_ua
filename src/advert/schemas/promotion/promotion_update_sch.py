from typing import Optional
from pydantic import BaseModel
from src.enums import TypeEnum
from .base_promotion_sch import PromotionBase

class PromotionUpdate(BaseModel):
    is_color: Optional[bool] = None
    is_big_advert: Optional[bool] = None
    add_frase: Optional[str] = None
    type_promotion: Optional[TypeEnum] = None
