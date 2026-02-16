from fastapi import APIRouter, status, HTTPException
from dishka.integrations.fastapi import FromDishka, inject

from src.advert.schemas.filters.filters_create_sch import FilterCreate
from src.advert.schemas.filters.filters_read_sch import  FilterRead
from src.advert.services.filter_serv import FilterService
from typing import Annotated
from src.users.models import User
from fastapi import Depends
from src.auth.dependencies import get_current_user

CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(tags=["Filters"])




@router.post("/search", status_code=status.HTTP_201_CREATED)
@inject
async def create_filter_and_search(
    filter_data: FilterCreate,
    service: FromDishka[FilterService],
    user: CurrentUser
):
    """Створює фільтр та повертає список оголошень."""
    return await service.create_filter_and_get_results(
        user_id=user.id,
        filter_dto=filter_data
    )