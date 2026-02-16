from fastapi import APIRouter,HTTPException, Depends
from dishka.integrations.fastapi import FromDishka,inject
from fastapi.security import HTTPBearer
from src.users.schemas.user.user_update import UserUpdate
from src.users.schemas.user.user_read import UserRead
from src.users.models.users import User
from src.auth.dependencies import get_current_user
from src.users.services.user_service import UserService
from src.auth.dependencies import get_current_user
from src.users.models.users import User
bearer_scheme = HTTPBearer()

router = APIRouter()

@router.put("/update/{user_id}", response_model=UserRead)
@inject
async def update_user(
    user_id: int,
    data: UserUpdate,
    user_service: FromDishka[UserService],
    current_user: User = Depends(get_current_user),):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: cannot update other user")

    updated_user = await user_service.update_user(user_id, data)
    return updated_user
