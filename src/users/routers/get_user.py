from fastapi import APIRouter,Depends
from dishka.integrations.fastapi import FromDishka, inject
from typing import List
from src.users.services.user_service import UserService
from src.users.schemas.user.user_read import UserRead
from src.users.models import User
from src.auth.dependencies import get_current_user
from fastapi import Header, HTTPException, Depends
from src.auth.services.auth_service import AuthService
from dishka.integrations.fastapi import inject, FromDishka
from fastapi import Query


router = APIRouter()


@router.get("/user/{user_id}", response_model=UserRead)
@inject
async def get_user(
    user_id: int,
    service: FromDishka[AuthService],
    token: str = Query(...),
):
    user = await service.get_user_by_token(token)
    if not user or user.id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
