from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.services.jwt_service import JWTService
from src.users.services.user_service import UserService
from src.users.models import User
from dishka.integrations.fastapi import FromDishka, inject

oauth2_scheme = HTTPBearer()


@inject
async def get_current_user(
    token_data: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    jwt_service: JWTService = Depends(),
    user_service: FromDishka[UserService] = Depends(FromDishka),
) -> User:
    token = token_data.credentials  # ← ИСПРАВЛЕНО

    try:
        payload = jwt_service.decode_token(token)
        user_id = getattr(payload, "user_id", None)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate token: {str(e)}",
        )

    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user