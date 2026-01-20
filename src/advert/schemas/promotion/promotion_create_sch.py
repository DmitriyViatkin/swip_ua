from typing import Optional
from pydantic import BaseModel
from src.enums import TypeEnum
from .base_promotion_sch import PromotionBase

# --- Базовая схема ---
class PromotionCreate(PromotionBase):
    add_frase: str  # Обязательное при создании
    advert_id: int