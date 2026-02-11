from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.building.schemas.chessboard_sch import ChessboardRow, ChessboardCell
from src.building.schemas.flat import FlatCreate, FlatRead
from src.building.models.flat import Flat
from src.building.models.floor import Floor

from src.building.services.chessboard_service import ChessboardService

router = APIRouter(prefix="/chessboard")

@router.post(
    "/add",
    response_model=FlatRead,
)
@inject
async def add_flat(
    data: FlatCreate,
    session: FromDishka[AsyncSession],
    service: FromDishka[ChessboardService],
):
    flat = await service.add_flat_to_chessboard(session=session, flat_data=data.dict())
    await session.commit()
    return flat