from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.advert.advert_update_sch import AdvertUpdate
from ..schemas.advert.advert_read_sch import AdvertRead
from ..services.advert_serv import AdvertService
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject

router = APIRouter()
@router.patch("/advert/{advert_id}", response_model= AdvertRead, status_code=status.HTTP_200_OK )
@inject

async def update_advert(
        advert_id: int,
        data: AdvertUpdate,
        session: FromDishka[AsyncSession],
        advert_service: FromDishka[AdvertService],
):
    advert_data = data.model_dump(exclude_unset=True)
    advert = await advert_service.update(advert_id, advert_data)
    return advert

