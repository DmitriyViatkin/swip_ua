from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.advert.advert_create_sch import AdvertCreate
from ..schemas.advert.advert_update_sch import AdvertUpdate
from ..schemas.advert.advert_read_sch import AdvertRead
from ..services.advert_serv import AdvertService
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject

router = APIRouter()
@router.post("/advert", response_model= AdvertRead, status_code=status.HTTP_201_CREATED )
@inject

async def create_advert(
        data: AdvertCreate,
        session: FromDishka[AsyncSession],
        advert_service: FromDishka[AdvertService],
):
        advert_data = data.dict()
        advert = await advert_service.create(advert_data)
        return advert

