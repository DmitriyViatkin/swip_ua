# src/building/routers/chessboard.py
from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
from  src.enums import UserRole
from src.users.models.users import User
from typing import Annotated

from src.building.schemas.chessboard_sch import ChessboardRow
from src.building.services.chessboard_service import ChessboardService

CurrentUser = Annotated[User, Depends(require_roles(UserRole.DEV,UserRole.CLIENT))]

router = APIRouter(prefix="/chessboard"  )


@router.get(
    "/section/{section_id}/{house_id}",
    response_model=list[ChessboardRow],
)
@inject
async def get_chessboard(
    section_id: int,
    house_id:int,
    user: CurrentUser,
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