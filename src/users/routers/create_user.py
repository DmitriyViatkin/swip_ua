from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from src.users.schemas.user.user_create import UserCreateSchema
from src.users.schemas.user.user_read import UserRead
from src.users.services.user_service import UserService

router = APIRouter()

@router.post("/user/create/")
@inject
async def create_user(data: UserCreateSchema, service: FromDishka[UserService]):
    return await service.create_user(data)
