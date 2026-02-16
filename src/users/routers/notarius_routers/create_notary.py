from fastapi import APIRouter, Depends
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject
from src.users.schemas.user.user_create import UserCreateSchema
from src.enums import UserRole
from src.users.services.user_service import UserService

router = APIRouter()

@router.post("/notary/create/")
@inject

async def create_notary(
    data: UserCreateSchema,
    service: FromDishka[UserService],
        current_user: User = Depends(get_current_user)
):
    return await service.create_user(
        data=data,
        role=UserRole.NOTARY,
    )