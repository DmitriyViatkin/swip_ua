from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.users.services.user_service import UserService
from typing import Annotated
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
from  src.enums import UserRole
CurrentUser = Annotated[User, Depends(require_roles(UserRole.CLIENT, UserRole.ADMIN))]


router = APIRouter()

@router.delete("/delete/{user_id}", response_model=dict)
@inject
async def delete_user(user_id: int, service: FromDishka[UserService],
                      user: CurrentUser):
    await service.delete_user(user_id)
    return {"status": "deleted"}