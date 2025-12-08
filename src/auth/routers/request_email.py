from fastapi import APIRouter, HTTPException
from src.auth.schemas.email_request import EmailRequest
from src.auth.utils.generate_code import generator

from dishka.integrations.fastapi import FromDishka, inject
from redis.asyncio import Redis
from src.auth.tasks import send_email_task


router = APIRouter(  )

@router.post("/request-email-code")
@inject
async def request_email_code(
    payload: EmailRequest,
    redis: FromDishka[Redis],
):
    email = payload.email


    code = generator()
    key = f"email_code:{email}"


    await redis.setex(key, 300, code)

    # TODO: отправка письма
    print(f"Код для {email}: {code}")
    send_email_task.delay(
        to_email=payload.email,
        subject="Код подтверждения",
        body=f"Ваш код : {code}"
    )

    return {"message": "Код отправлен на email"}