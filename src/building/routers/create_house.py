from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.building.schemas.house import HouseCreate, HouseRead
from src.building.services.house import HouseService
from src.users.models.users import User
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/houses", response_model=HouseRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_house(
    data: HouseCreate,
    session: FromDishka[AsyncSession],
    house_service: FromDishka[HouseService],
    current_user: User = Depends(get_current_user),
):
    house_data = data.dict()
    house_data['user_id'] = current_user.id
    house = await house_service.create(session, house_data)
    return house