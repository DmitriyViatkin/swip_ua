from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka

from src.users.schemas.user_create import UserCreateSchema
from src.users.schemas.user_read import UserRead
from src.users.services.user_service import UserService

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(data: UserCreateSchema, service: UserService = FromDishka()):
    return await service.create_user(data)
