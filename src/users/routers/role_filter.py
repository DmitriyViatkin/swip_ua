from typing import List
from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from src.enums import UserRole
from src.users.schemas.user.user_read import UserRead
from src.users.services.user_service import UserService

router = APIRouter()

@router.get("users/role/{role}", response_model=List[UserRead])
@inject
async def get_by_role(role: UserRole, service: FromDishka[UserService]):
    return await service.get_user_by_role(role)
