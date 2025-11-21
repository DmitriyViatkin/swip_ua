from typing import List
from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka

from src.enums import UserRole
from src.users.schemas.user_read import UserRead
from src.users.services.user_service import UserService

router = APIRouter()

@router.get("/role/{role}", response_model=List[UserRead])
async def get_by_role(role: UserRole, service: UserService = FromDishka()):
    return await service.get_user_by_role(role)
