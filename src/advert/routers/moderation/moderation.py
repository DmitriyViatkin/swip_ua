from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.advert.advert_update_sch import AdvertUpdate
from ... schemas.advert.advert_read_sch import AdvertRead
from ... services.advert_serv import AdvertService
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject

router = APIRouter()


@router.put(
    "/admin/{advert_id}/approved",
    response_model=AdvertRead,
    status_code=status.HTTP_200_OK
)
@inject
async def set_moderation (
    advert_id: int,
    advert_service: FromDishka[AdvertService],
):
    adverts = await advert_service.moderation(advert_id)
    return adverts