from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.auth.services.jwt_service import JWTService
from src.users.services.user_service import UserService
from src.users.models import User
from dishka.integrations.fastapi import FromDishka, inject

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authorization/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    jwt_service: JWTService = Depends(),
    user_service: FromDishka[UserService] = Depends(FromDishka)
) -> User:
    try:
        payload = jwt_service.decode_token(token)

        # FIX: токен содержит поле "user_id", а не "sub"
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: no user_id"
            )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token"
        )

    user = await user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return user