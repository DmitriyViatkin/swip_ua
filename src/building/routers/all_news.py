from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.fastapi import FromDishka, inject

from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
from  src.enums import UserRole
from src.users.models.users import User
from src.building.schemas.news import NewsRead
from src.building.services.news import NewsService
from src.building.services.house import HouseService

router = APIRouter()


@router.get(
    "/houses/{house_id}/news",
    response_model=list[NewsRead],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_house_news(
    house_id: int,
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

    # 3. Получаем новости дома
    news_list = await news_service.get_all_by_house(
        session=session,
        house_id=house_id,
    )

    return news_list
