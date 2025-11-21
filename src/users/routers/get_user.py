from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka
from src.users.schemas.user.user_read import UserRead
from src.users.services.user_service import UserService

router = APIRouter()

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, service: UserService = FromDishka(UserService)):
    return await service.get_user(user_id)
