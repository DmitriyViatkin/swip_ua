from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dishka.integrations.fastapi import FromDishka, inject
from src.users.schemas.user.user_read import UserRead
from src.auth.dependencies import get_current_user
from src.auth.services.auth_service import AuthService
from src.users.models.users import User
from src.building.services.personal_cabinet_service import PersonalCabinetService
from src.building.schemas.personal_cabinet import PersonalCabinet
bearer_scheme = HTTPBearer()

router = APIRouter()

@router.get("/developer/{user_id}", response_model=PersonalCabinet)
@inject
async def get_personal_cabinet(
    user_id: int,
    service: FromDishka[PersonalCabinetService],
    current_user: User = Depends(get_current_user),
):
    data = await service.get_personal_cabinet(user_id)

    if not data.user:
        raise HTTPException(status_code=404, detail="User not found")

    return data