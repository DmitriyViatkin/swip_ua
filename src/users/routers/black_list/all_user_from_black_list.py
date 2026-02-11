from fastapi import APIRouter,Depends,HTTPException
from dishka.integrations.fastapi import FromDishka,inject
from typing import List
from src.users.services.user_service import UserService
from src.users.services.black_list_serv import BlackListService
from src.users.schemas.black_list.read import BlackListRead, UserBlackList
from src.auth.services.auth_service import AuthService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from fastapi_pagination import Page, paginate


bearer_scheme = HTTPBearer()
router = APIRouter()

@router.get("/all_users_from_blacklist", response_model= Page[UserBlackList])
@inject
async def get_all_users(
   # current_user: User = Depends(get_current_user),
    user_service: FromDishka[UserService] = Depends(),
):
    users = await user_service.get_blocked_user()
    return  paginate (users)


















