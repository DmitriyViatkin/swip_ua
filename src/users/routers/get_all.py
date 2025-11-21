from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka,inject
from typing import List
from src.users.services.user_service import UserService
from src.users.schemas.user.user_read import UserRead



router = APIRouter()


from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import FromDishka, inject
from typing import List

from src.users.services.user_service import UserService
from src.users.schemas.user.user_read import UserRead

router = APIRouter()

@router.get("/", response_model=List[UserRead])
@inject
async def get_all_users(service: FromDishka[UserService]):
    users = await service.get_all_users()
    return users