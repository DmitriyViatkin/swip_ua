from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from dishka.integrations.fastapi import FromDishka, inject

from src.users.services.favorite_serv import FavoritesService
from src.users.schemas.favorite.favorite_create_sch import FavoriteCreate
from src.users.schemas.favorite.favorite_read_sch import FavoriteRead
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from fastapi_pagination import  Page, paginate

router = APIRouter( )





@router.get(
    "/me",
    response_model=Page[FavoriteRead]
)
@inject
async def get_my_favorites(
        service: FromDishka[FavoritesService],
        user: User = Depends(get_current_user),

):
    favorites = await service.get_my_favorites(user.id)
    return paginate(favorites)

