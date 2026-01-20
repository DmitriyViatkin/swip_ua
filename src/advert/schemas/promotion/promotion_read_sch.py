from .base_promotion_sch import PromotionBase

class PromotionRead(PromotionBase):
    id: int


    model_config = {
        "from_attributes": True
    }