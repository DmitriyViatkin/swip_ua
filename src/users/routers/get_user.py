from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dishka.integrations.fastapi import FromDishka, inject
from src.users.schemas.user.user_read import UserRead
from src.auth.dependencies import get_current_user
from src.auth.services.auth_service import AuthService
from src.users.models.users import User
from src.users.services.user_service import UserService
bearer_scheme = HTTPBearer()

router = APIRouter()

@router.get("/user/{user_id}", response_model=UserRead)
@inject
async def get_user(
    user_id: int,
    user_service: FromDishka[UserService],
    current_user: User = Depends(get_current_user),
):
    user = await user_service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
