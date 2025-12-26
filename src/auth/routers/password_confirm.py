from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka, inject
from config.infra.providers.reset_password_provider import  PasswordResetServiceProvider
from src.auth.schemas.password_reset_confirm import  PasswordResetConfirm
from src.auth.services.reset_password_service import PasswordResetService


router = APIRouter()




@router.post("/reset-password")
@inject
async def reset_password(
    data: PasswordResetConfirm,
    service: FromDishka[PasswordResetService],
):
    return await service.reset_password(data.token, data.new_password)