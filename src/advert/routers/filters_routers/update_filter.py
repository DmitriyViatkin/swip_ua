from src.advert.schemas.filters.filters_update_sch import FilterUpdate
from src.advert.schemas.filters.filters_read_sch import FilterRead
from dishka.integrations.fastapi import FromDishka, inject
from src.advert.services.filter_serv import FilterService
from fastapi import  HTTPException,APIRouter, status
from typing import Annotated
from src.users.models import User
from fastapi import Depends
from src.auth.dependencies import get_current_user
# Ось це визначення аліаса:
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(  tags=["Filters"])

@router.patch("/{filter_id}", response_model=FilterRead)
@inject
async def patch_filter(
    filter_id: int,
    update_data: FilterUpdate,
    service: FromDishka[FilterService],
    user: CurrentUser
):
    """Оновлення фільтра (тільки власником)."""
    updated_filter = await service.update_filter(
        filter_id=filter_id,
        user_id=user.id,
        update_data=update_data
    )
    if not updated_filter:
        raise HTTPException(status_code=404, detail="Фільтр не знайдено")
    return updated_filter