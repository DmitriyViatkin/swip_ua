from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.advert.advert_update_sch import AdvertUpdate
from ..schemas.advert.advert_read_sch import AdvertRead
from ..services.advert_serv import AdvertService
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from typing import Annotated
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter()


@router.delete(
    "/advert/{advert_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_advert(
    advert_id: int,
    user: CurrentUser,
    advert_service: FromDishka[AdvertService],
):
    await advert_service.delete(advert_id)
