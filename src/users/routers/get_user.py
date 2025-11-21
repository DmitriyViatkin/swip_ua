from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject
from typing import List
from src.users.services.user_service import UserService
from src.users.schemas.user.user_read import UserRead

router = APIRouter()

@router.get("/user/{user_id}",response_model=UserRead)
@inject
async def get_user(user_id:int, service: FromDishka[UserService]):

    return await service.get_user( user_id)
