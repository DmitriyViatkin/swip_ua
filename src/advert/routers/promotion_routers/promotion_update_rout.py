
from fastapi import APIRouter, status, HTTPException

from dishka.integrations.fastapi import FromDishka, inject
from src.advert.services.promotion_serv import PromotionService
from src.advert.schemas.promotion.promotion_read_sch import PromotionRead
from src.advert.schemas.promotion.promotion_update_sch import PromotionUpdate


router = APIRouter()


@router.put("/{advert_id}/promotion", response_model=PromotionRead)
@inject
async def update_promotion_handler(
        advert_id: int,
        data: PromotionUpdate,
        promotion_service: FromDishka[PromotionService],
):
    """Обновление промоушена через сервис"""


    update_data = data.model_dump(exclude_unset=True, exclude={'advert_id'})


    updated_promotion = await promotion_service.update_by_advert_id(advert_id, update_data)


    if not updated_promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Promotion for advert {advert_id} not found"
        )

    return updated_promotion