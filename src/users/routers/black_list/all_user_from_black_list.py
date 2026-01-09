from fastapi import APIRouter,Depends,HTTPException
from dishka.integrations.fastapi import FromDishka,inject
from typing import List
from src.users.services.user_service import UserService
from src.users.services.black_list_serv import BlackListService
from src.users.schemas.black_list.read import BlackListRead
from src.auth.services.auth_service import AuthService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.dependencies import get_current_user
from src.users.models.users import User



bearer_scheme = HTTPBearer()
router = APIRouter()

@router.get("/all_users_from_blacklist", response_model=List[BlackListRead])
@inject
async def get_all_users(
    current_user: User = Depends(get_current_user),
    user_service: FromDishka[BlackListService] = Depends(),
):
    return await user_service.get_all_blocked_users()


















