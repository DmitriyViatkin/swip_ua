from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.advert.advert_update_sch import AdvertUpdate
from ... schemas.advert.advert_read_sch import AdvertRead
from ... services.advert_serv import AdvertService
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from typing import Annotated
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter()


@router.put(
    "/admin/{advert_id}/deapproved",
    response_model=AdvertRead,
    status_code=status.HTTP_200_OK
)
@inject
async def set_unmoderation (
    advert_id: int,
    user:CurrentUser,
    advert_service: FromDishka[AdvertService],
):
    adverts = await advert_service.unModeration(advert_id)
    return adverts