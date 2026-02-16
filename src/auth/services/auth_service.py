from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.exc import SQLAlchemyError

from src.auth.security.password import verify_password
from src.auth.services.jwt_service import JWTService
from src.users.schemas.user.user_read import UserRead
from src.users.schemas.user.login_sch import UserLoginRead


class AuthService:
    def __init__(self, user_repository, jwt_service: JWTService):
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    # ---------------- AUTHENTICATE ----------------

    async def authenticate(self, username: str, password: str) -> UserLoginRead:
        try:
            user = await self.user_repository.get_by_email_or_phone(username)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error"
            )

        # ❗ Не раскрываем, существует ли пользователь
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        return UserLoginRead.model_validate(user)

    # ---------------- TOKENS ----------------

    def create_tokens(self, user: UserRead) -> dict:
        data = {
            "user_id": user.id,
            "email": user.email,
        }

        return {
            "access_token": self.jwt_service.create_access_token(data),
            "refresh_token": self.jwt_service.create_refresh_token(data),
            "token_type": "bearer"
        }

    # ---------------- GET USER BY TOKEN ----------------

    async def get_user_by_token(self, token: str) -> UserRead:
        try:
            payload = self.jwt_service.decode_token(token)

            # ✅ Безопасное получение значения
            user_id = payload.get("user_id")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )

        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        except Exception:
            # 🔥 защита от неожиданных ошибок
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

        user = await self.user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

        return user
