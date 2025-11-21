from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka

from src.users.services.user_service import UserService

router = APIRouter()

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, service: UserService = FromDishka()):
    await service.delete_user(user_id)
    return {"status": "deleted"}