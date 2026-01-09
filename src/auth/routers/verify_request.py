from fastapi import APIRouter, HTTPException
from src.auth.schemas.verify_request import VerifyRequest
from dishka.integrations.fastapi import FromDishka, inject
from src.users.services.user_service import UserService
from redis.asyncio import Redis

router = APIRouter( )


@router.post("/verify-email")
@inject
async def verify_email(
    payload: VerifyRequest,
    redis: FromDishka[Redis],
    user_service: FromDishka[UserService],
):
    email = payload.email
    key = f"email_code:{email}"

    saved_code = await redis.get(key)

    if not saved_code:
        raise HTTPException(status_code=400, detail="Код истёк или не найден")

    if saved_code.decode("utf-8") if isinstance(saved_code, bytes) else saved_code != payload.code:
        raise HTTPException(status_code=400, detail="Неверный код")


    user = await user_service.user_repository.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


    updated_user = await user_service.email_verified(user.id)


    await redis.delete(key)

    return {
        "success": True,
        "message": "Email подтвержден",
        "user": updated_user
    }