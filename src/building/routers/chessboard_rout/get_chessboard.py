# src/building/routers/chessboard.py
from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.building.schemas.chessboard_sch import ChessboardRow
from src.building.services.chessboard_service import ChessboardService

router = APIRouter(prefix="/chessboard"  )


@router.get(
    "/section/{section_id}/{house_id}",
    response_model=list[ChessboardRow],
)
@inject
async def get_chessboard(
    section_id: int,
        house_id:int,
    session: FromDishka[AsyncSession],
    service: FromDishka[ChessboardService],
):
    """
    Получение шахматки по секции
    """
    return await service.get_section_chessboard(
        session=session,
        section_id=section_id,
    house_id = house_id
    )