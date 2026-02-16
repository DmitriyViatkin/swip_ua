from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dishka.integrations.fastapi import FromDishka, inject
from src.users.schemas.user.user_read import UserRead

from src.users.models.users import User
from src.users.services.user_service import UserService

from  src.enums import UserRole
from typing import Annotated
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
CurrentUser = Annotated[User, Depends(require_roles(UserRole.CLIENT, UserRole.ADMIN))]

router = APIRouter()

@router.get("/user/{user_id}", response_model=UserRead)
@inject
async def get_user(
    user_id: int,
    user_service: FromDishka[UserService],
    user: CurrentUser,
):
    user = await user_service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
