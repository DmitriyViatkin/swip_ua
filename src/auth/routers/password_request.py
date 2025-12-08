from fastapi import APIRouter, Depends, HTTPException
from dishka.integrations.fastapi import FromDishka, inject
from config.infra.providers.reset_password_provider import  PasswordResetServiceProvider
from src.auth.schemas.password_reset import PasswordResetRequest
from src.auth.services.reset_password_service import PasswordResetService


router = APIRouter()

@router.post("/request-password-reset")
@inject
async def request_password_reset(
    data: PasswordResetRequest,
    service: FromDishka[PasswordResetService],   # <- правильно
):
    user = await service.user_repo.get_by_email_or_phone(data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    token = service.generate_reset_token(user.email)

    return {"msg": "Ссылка для восстановления пароля отправлена", "token": token}


