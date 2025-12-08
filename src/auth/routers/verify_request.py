from fastapi import APIRouter
from src.auth.schemas.verify_request import VerifyRequest
from dishka.integrations.fastapi import FromDishka, inject
from redis.asyncio import Redis

router = APIRouter( )


@router.post("/verify-email")
@inject
async def verify_email(
    payload: VerifyRequest,
    redis: FromDishka[Redis],
):
    email = payload.email
    key = f"email_code:{email}"

    saved_code = await redis.get(key)

    if not saved_code:
        return {"success": False, "message": "Код истёк или не найден"}

    if saved_code != payload.code:
        return {"success": False, "message": "Неверный код"}


    await redis.delete(key)

    return {"success": True, "message": "Email подтвержден"}