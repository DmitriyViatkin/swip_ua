from fastapi import APIRouter,Depends,HTTPException
from dishka.integrations.fastapi import FromDishka,inject
from typing import List
from src.users.services.user_service import UserService
from src.users.schemas.user.user_read import UserRead
from src.auth.services.auth_service import AuthService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.dependencies import get_current_user
from src.users.models.users import User



bearer_scheme = HTTPBearer()
router = APIRouter()

@router.get("/notary", response_model=List[UserRead])
@inject
async def get_all_notary(
    current_user: User = Depends(get_current_user),
    user_service: FromDishka[UserService] = Depends(),
):
    return await user_service.get_all_users()