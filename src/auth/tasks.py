from email.message import EmailMessage
import aiosmtplib
import asyncio

from config.infra.config.settings import infra_settings
from config.infra.utils.celery_app import celery_app


@celery_app.task
def send_email_task(to_email: str, subject: str, body: str):
    async def _send():
        msg = EmailMessage()
        from_email = infra_settings.smtp.FROM_EMAIL
        print("FROM_EMAIL:", repr(from_email))  # для дебагу

        if not from_email:
            raise ValueError("FROM_EMAIL не може бути пустим або None")

        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        await aiosmtplib.send(
            msg,
            hostname=infra_settings.smtp.HOST,
            port=infra_settings.smtp.PORT,
            username=infra_settings.smtp.USER,
            password=infra_settings.smtp.PASSWORD,
            start_tls=infra_settings.smtp.USE_TLS,
        )

    asyncio.run(_send())

@celery_app.task
def send_reset_password_email(email: str, token: str):
    reset_link = f"http://frontend/reset-password?token={token}&email={email}"
    print(f"Отправить ссылку для сброса пароля: {reset_link}")
