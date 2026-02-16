from fastapi import APIRouter,Depends,HTTPException
from dishka.integrations.fastapi import FromDishka,inject
from typing import List
from src.users.services.user_service import UserService
from src.users.schemas.user.user_read import UserRead, UserList
from src.auth.services.auth_service import AuthService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from fastapi_pagination import  Page, paginate
from src.users.models.users import User
from  src.enums import UserRole
from typing import Annotated
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
CurrentUser = Annotated[User, Depends(require_roles( UserRole.ADMIN))]

bearer_scheme = HTTPBearer()
router = APIRouter()

@router.get("/all_user", response_model= Page[UserList])
@inject
async def get_all_users(
    user: CurrentUser,
    user_service: FromDishka[UserService] = Depends(),
):
    users = await user_service.get_all_users()


    return paginate(users)