from typing import Optional
from pydantic import BaseModel
from src.enums import TypeEnum

# --- Базовая схема ---
class PromotionBase(BaseModel):
    add_frase: Optional[str] = None
    is_color: Optional[bool] = False
    is_big_advert: Optional[bool] = False
    type_promotion: Optional[TypeEnum] = None
    advert_id: Optional[int] = None