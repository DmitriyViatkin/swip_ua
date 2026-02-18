from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.fastapi import FromDishka, inject

from src.building.services.house import HouseService
from src.building.schemas.house import HouseRead
from src.users.models.users import User
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
from  src.enums import UserRole
router = APIRouter()


@router.get("/houses/{house_id}", response_model=HouseRead, status_code=status.HTTP_200_OK)
@inject
async def get_house(
        house_id: int,
        session: FromDishka[AsyncSession],
        house_service: FromDishka[HouseService],
        current_user: User = Depends(require_roles(UserRole.DEV,UserRole.CLIENT)),
):
    # 1️⃣ получаем дом с selectinload всех связанных сущностей
    house = await house_service.get_by_id(session=session, pk=house_id)

    if not house:
        raise HTTPException(status_code=404, detail="House not found")


    if house.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return house
