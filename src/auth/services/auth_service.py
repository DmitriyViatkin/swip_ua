from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from src.auth.security.password import verify_password
from src.auth.services.jwt_service import JWTService
from src.users.schemas.user.user_read import UserRead
from src.users.schemas.user.login_sch import UserLoginRead

class AuthService:
    def __init__(self, user_repository, jwt_service: JWTService):
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def authenticate(self, username: str, password: str) -> UserRead:
        user = await self.user_repository.get_by_email_or_phone(username)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        return UserLoginRead.model_validate(user)

    def create_tokens(self, user: UserRead) -> dict:
        data = {
            "user_id": user.id,
            "email": user.email,
        }
        access_token = self.jwt_service.create_access_token(data)
        refresh_token = self.jwt_service.create_refresh_token(data)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def get_user_by_token(self, token: str) -> UserRead:
        try:
            payload = self.jwt_service.decode_token(token)
            user_id = payload.user_id
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
