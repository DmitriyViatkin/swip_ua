from fastapi import APIRouter, HTTPException,status, Depends
from dishka.integrations.fastapi import FromDishka, inject
from src.users.models.users import User
from  src.enums import UserRole
from typing import Annotated
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
CurrentUser = Annotated[User, Depends(require_roles( UserRole.ADMIN))]
from src.users.schemas.black_list.create import BlackListCreate

from src.users.services.user_service import UserService

router = APIRouter( )

@router.put("/blacklist/remove/")
@inject
async def remove_from_black_list(data: BlackListCreate,
                                 user: CurrentUser,
                                 service: FromDishka[UserService]):
    result = await service.de_blocked_user(data.user_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {data.user_id} not found"
        )
    return result
