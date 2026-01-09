from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.advert.advert_update_sch import AdvertUpdate
from ..schemas.advert.advert_read_sch import AdvertRead
from ..services.advert_serv import AdvertService
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject

router = APIRouter()


@router.get(
    "/adverts/{advert_id}",
    response_model=AdvertRead,
    status_code=status.HTTP_200_OK
)
@inject
async def get_advert_by_id(
    advert_id: int,
    advert_service: FromDishka[AdvertService],
):
    adverts = await advert_service.get_by_id(advert_id)
    return adverts