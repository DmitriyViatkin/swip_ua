from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
from  src.enums import UserRole
from src.users.models.users import User
from src.building.schemas.news import NewsUpdate, NewsRead
from src.building.services.news import NewsService
from src.building.services.house import HouseService

router = APIRouter()


@router.put("/houses/{house_id}/news/{news_id}", response_model=NewsRead, status_code=status.HTTP_200_OK,)
@inject
async def update_news( house_id: int, news_id: int,  data: NewsUpdate, session: FromDishka[AsyncSession],
                        news_service: FromDishka[NewsService], house_service: FromDishka[HouseService],
                       current_user: User = Depends(require_roles(UserRole.DEV)),):

    house = await house_service.get_by_id(session, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")


    if house.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")


    news = await news_service.get_by_id(session, news_id)
    if not news or news.house_id != house_id:
        raise HTTPException(status_code=404, detail="News not found")


    updated_news = await news_service.update(
        session=session,
        pk=news_id,
        data=data.dict(exclude_unset=True),
    )

    return updated_news
