from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.advert.advert_update_sch import AdvertUpdate
from ... schemas.advert.advert_read_sch import AdvertRead
from ... services.advert_serv import AdvertService
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject
from typing import List


router = APIRouter()


@router.get(
    "/adverts/all_advert_moderation",
    response_model=List[AdvertRead],
    status_code=status.HTTP_200_OK
)
@inject
async def all_advert_moderation (

    advert_service: FromDishka[AdvertService],
):
    adverts = await advert_service.get_ads_to_moderate()
    return adverts