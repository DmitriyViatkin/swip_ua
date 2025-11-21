from typing import List
from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka

from src.users.services.user_service import UserService
from src.users.schemas.user.user_read import UserRead

router = APIRouter()

@router.get("/", response_model=List[UserRead])
async def get_all(service: UserService = FromDishka()):
    return await service.get_all_users()