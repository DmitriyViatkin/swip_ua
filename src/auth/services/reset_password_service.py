from itsdangerous import URLSafeTimedSerializer
from datetime import timedelta
from fastapi import HTTPException, status
from src.auth.services.jwt_service import JWTService
from src.auth.security.password import hash_password, verify_password
from src.users.repositories.user_repository import UserRepository
from src.users.schemas.user.user_read import UserRead

RESET_PASSWORD_SALT = "password-reset-salt"
RESET_PASSWORD_EXPIRE_HOURS = 1

class PasswordResetService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.serializer = URLSafeTimedSerializer(JWTService().secret_key)

    def generate_reset_token(self, email: str) -> str:
        """Создает токен сброса пароля для email"""
        return self.serializer.dumps(email, salt=RESET_PASSWORD_SALT)

    def verify_reset_token(self, token: str) -> str:
        """Проверяет токен, возвращает email или вызывает HTTPException"""
        try:
            email = self.serializer.loads(token, salt=RESET_PASSWORD_SALT, max_age=RESET_PASSWORD_EXPIRE_HOURS*3600)
            return email
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный или просроченный токен")

    async def reset_password(self, token: str, new_password: str):
        # 1. Проверяем токен
        email = self.verify_reset_token(token)

        # 2. Ищем пользователя
        user = await self.user_repo.get_by_email_or_phone(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

        # 3. Хэшируем пароль
        hashed = hash_password(new_password)

        # 4. Обновляем пароль — только 1 раз
        await self.user_repo.update_password(user.id, hashed)

        return {"msg": "Пароль успешно обновлен"}