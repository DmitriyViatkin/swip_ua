
from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import FromDishka, inject

from src.users.schemas.black_list.create import BlackListCreate

from src.users.services.user_service import UserService

router = APIRouter(tags=["Blacklist"])

@router.put("/blacklist/blocked_user/")
@inject
async def add_to_black_list(data: BlackListCreate, service: FromDishka[UserService]):
    result = await service.blocked_user(data.user_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {data.user_id} not found"
        )
    return result