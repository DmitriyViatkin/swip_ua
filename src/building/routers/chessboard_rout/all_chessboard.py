# src/building/routers/chessboard.py
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


@router.get(
    "/full/",
    response_model=list[ChessboardRow],
)
@inject
async def get_chessboard_full(

    session: FromDishka[AsyncSession],
    service: FromDishka[ChessboardService],
):
    return await service.get_all_chessboards(session=session)