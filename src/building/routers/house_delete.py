from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.building.schemas.house import HouseUpsert, HouseRead
from src.building.services.house import HouseService
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.dependencies import get_current_user

router = APIRouter()


@router.delete("/houses/{house_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_house(
        house_id: int,
        session: FromDishka[AsyncSession],
        house_service: FromDishka[HouseService],
        current_user: User = Depends(get_current_user),
):
    house = await house_service.get_by_id(session, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    if house.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    await house_service.delete(session, house_id)
    return None