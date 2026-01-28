from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import FromDishka, inject

from src.advert.services.promotion_serv import PromotionService
from src.advert.schemas.promotion.promotion_read_sch import PromotionRead
from src.advert.schemas.promotion.promotion_update_sch import PromotionUpdate

router = APIRouter( )


@router.put("/{advert_id}/promotion", response_model=PromotionRead)
@inject
async def update_promotion(
    advert_id: int,
    data: PromotionUpdate,
    service: FromDishka[PromotionService],
):
    update_data = data.model_dump(exclude_unset=True)

    promotion = await service.update_by_advert_id(
        advert_id=advert_id,
        data=update_data
    )

    if not promotion:
        raise HTTPException(
            status_code=404,
            detail=f"Promotion for advert {advert_id} not found"
        )

    return promotion
