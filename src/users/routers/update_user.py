from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka

from src.users.schemas.user_update import UserUpdateSchema
from src.users.schemas.user_read import UserRead
from src.users.services.user_service import UserService

router = APIRouter()

@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdateSchema,
    service: UserService = FromDishka()
):
    return await service.update_user(user_id, data)
