from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from dishka.integrations.fastapi import FromDishka, inject

from src.users.services.favorite_serv import FavoritesService
from src.users.schemas.favorite.favorite_create_sch import FavoriteCreate
from src.users.schemas.favorite.favorite_read_sch import FavoriteRead
from src.auth.dependencies  import get_current_user
from src.users.models.users import User
from src.users.models.users import User
from  src.enums import UserRole
from typing import Annotated
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
CurrentUser = Annotated[User, Depends(require_roles(UserRole.CLIENT, UserRole.ADMIN))]

router = APIRouter( )


@router.post(
    "/add",
    response_model=FavoriteRead,
    status_code=status.HTTP_201_CREATED
)
@inject
async def add_to_favorites(
    data: FavoriteCreate,
    service: FromDishka[FavoritesService],
    user: CurrentUser,

):
    favorite = await service.add_to_favorites(user.id, data)

    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Оголошення вже в обраному"
        )

    return favorite

