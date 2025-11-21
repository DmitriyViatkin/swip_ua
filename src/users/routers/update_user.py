from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka,inject

from src.users.schemas.user.user_update import UserUpdate
from src.users.schemas.user.user_read import UserRead
from src.users.services.user_service import UserService

router = APIRouter()

@router.put("/update/{user_id}", response_model=UserRead)
@inject
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: FromDishka[UserService]
):
    return await service.update_user(user_id, data)
