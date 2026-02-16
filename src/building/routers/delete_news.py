from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.fastapi import FromDishka, inject

from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
from  src.enums import UserRole
from src.users.models.users import User
from src.building.services.news import NewsService
from src.building.services.house import HouseService

router = APIRouter()


@router.delete(
    "/houses/{house_id}/news/{news_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_news(
    house_id: int,
    news_id: int,
    session: FromDishka[AsyncSession],
    news_service: FromDishka[NewsService],
    house_service: FromDishka[HouseService],
    current_user: User = Depends(require_roles(UserRole.DEV)),
):
    # 1. Проверяем дом
    house = await house_service.get_by_id(session, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    # 2. Проверяем владельца
    if house.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # 3. Проверяем новость
    news = await news_service.get_by_id(session, news_id)
    if not news or news.house_id != house_id:
        raise HTTPException(status_code=404, detail="News not found")

    # 4. Удаляем
    await news_service.delete(session, news_id)

    return None
