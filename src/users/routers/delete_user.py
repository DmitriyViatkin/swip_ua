from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from src.users.services.user_service import UserService

router = APIRouter()

@router.delete("/delete/{user_id}", response_model=dict)
@inject
async def delete_user(user_id: int, service: FromDishka[UserService]):
    await service.delete_user(user_id)
    return {"status": "deleted"}