from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from dishka.integrations.fastapi import FromDishka, inject

from src.users.services.favorite_serv import FavoritesService
from src.users.schemas.favorite.favorite_create_sch import FavoriteCreate
from src.users.schemas.favorite.favorite_read_sch import FavoriteRead
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.users.models.users import User
from  src.enums import UserRole
from typing import Annotated
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
CurrentUser = Annotated[User, Depends(require_roles(UserRole.CLIENT, UserRole.ADMIN))]

router = APIRouter( )




@router.delete(
    "/{advert_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def remove_from_favorites(
        advert_id: int,
        service: FromDishka[FavoritesService],
        user: CurrentUser,

):
    deleted = await service.remove_from_favorites(user.id, advert_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Оголошення не знайдено в обраному"
        )