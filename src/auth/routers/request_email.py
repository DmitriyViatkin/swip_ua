from fastapi import APIRouter, HTTPException
from src.auth.schemas.email_request import EmailRequest
from src.auth.utils.generate_code import generator
from src.users.services.user_service import UserService
from dishka.integrations.fastapi import FromDishka, inject
from redis.asyncio import Redis
from src.auth.tasks import send_email_task


router = APIRouter(  )

@router.post("/request-email-code")
@inject
async def request_email_code(
    payload: EmailRequest,
    redis: FromDishka[Redis],
    service: FromDishka[UserService]
):

    user = await service.check_user_before_code_request(payload.email)
    email = payload.email


    code = generator()
    key = f"email_code:{email}"


    await redis.setex(key, 300, code)

    #   отправка письма

    send_email_task.delay(
        to_email=payload.email,
        subject="Код подтверждения",
        body=f"Ваш код : {code}"
    )

    return {"message": "Код отправлен на email"}