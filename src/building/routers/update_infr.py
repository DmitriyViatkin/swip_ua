from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dishka.integrations.fastapi import FromDishka, inject
from src.users.schemas.user.user_read import UserRead
from src.auth.dependencies import get_current_user
from src.auth.services.auth_service import AuthService
from src.users.models.users import User
from src.building.services.infrastructure import InfrastructureService
from sqlalchemy.ext.asyncio import AsyncSession
from src.building.schemas.infrastructure import InfrastructureRead, InfrastructureUpdate
#bearer_scheme = HTTPBearer()

router = APIRouter()


@router.patch(
    "/houses/{house_id}/infrastructure",
    response_model=InfrastructureRead,
)
@inject
async def update_infrastructure(
    house_id: int,
    data: InfrastructureUpdate,
    service: FromDishka[InfrastructureService],
    # Добавляем сессию из Dishka
    session: FromDishka[AsyncSession],
    current_user: User = Depends(get_current_user),
):
    infrastructure = await service.update_or_create(
        session=session,
        house_id=house_id,
        data=data.model_dump(exclude_unset=True),
    )

    await session.commit()
    return infrastructure