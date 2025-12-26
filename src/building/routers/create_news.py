from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.fastapi import FromDishka, inject

from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.building.schemas.news import NewsCreate, NewsRead
from src.building.services.news import NewsService
from src.building.services.house import HouseService

router = APIRouter()


@router.post("/houses/{house_id}/news", response_model=NewsRead, status_code=status.HTTP_201_CREATED,)
@inject
async def create_news(
    house_id: int,
    data: NewsCreate,
    session: FromDishka[AsyncSession],
    news_service: FromDishka[NewsService],
    house_service: FromDishka[HouseService],
    current_user: User = Depends(get_current_user),
):

    house = await house_service.get_by_id(session, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")


    if house.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")


    news_data = data.dict()
    news_data["house_id"] = house_id

    news = await news_service.create(session, news_data)
    return news