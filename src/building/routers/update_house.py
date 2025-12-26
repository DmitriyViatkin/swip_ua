from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.building.schemas.house import HouseUpsert, HouseRead
from src.building.services.house import HouseService
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.dependencies import get_current_user

router = APIRouter()

@router.put("/houses/{house_id}", response_model=HouseRead, status_code=status.HTTP_200_OK)
@inject
async def update_house(
    house_id: int,
    data: HouseUpsert,
    session: FromDishka[AsyncSession],
    house_service: FromDishka[HouseService],
    current_user: User = Depends(get_current_user),
):

    house = await house_service.update(session, house_id, data.dict())

    if not house:

        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="House not found")


    if house.user_id != current_user.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Forbidden")

    return house