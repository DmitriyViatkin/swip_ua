import base64
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, status, HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.fastapi import FromDishka, inject
from src.advert.schemas.promotion.promotion_create_sch import PromotionCreate
from src.advert.schemas.promotion.promotion_read_sch import PromotionRead
from src.advert.schemas.advert.advert_read_sch import AdvertRead
from src.advert.services.promotion_serv import PromotionService
from src.advert.services.advert_serv import AdvertService
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from typing import Annotated
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter()


@router.post(
    "/advert/{advert_id}/promotion",
    response_model=PromotionRead,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_promotion(
        advert_id: int,
        user: CurrentUser,
        data: PromotionCreate,
        promotion_service: FromDishka[PromotionService],
):

    promotion_dict = data.model_dump()


    promotion_dict["advert_id"] = advert_id


    result = await promotion_service.create(promotion_dict)

    if not result:
        raise HTTPException(status_code=400, detail="Ошибка создания")

    return result