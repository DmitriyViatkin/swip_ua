# src/building/routers/chessboard.py
from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.building.schemas.chessboard_sch import ChessboardRow, ChessboardCell
from src.building.schemas.flat import FlatCreate, FlatRead
from src.building.models.flat import Flat
from src.building.models.floor import Floor
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
from  src.enums import UserRole
from src.users.models.users import User
from typing import Annotated
CurrentUser = Annotated[User, Depends(require_roles(UserRole.DEV,UserRole.CLIENT))]

from src.building.services.chessboard_service import ChessboardService

router = APIRouter(prefix="/chessboard")


@router.get(
    "/full/",
    response_model=list[ChessboardRow],
)
@inject
async def get_chessboard_full(
    user: CurrentUser,
    session: FromDishka[AsyncSession],
    service: FromDishka[ChessboardService],
):
    return await service.get_all_chessboards(session=session)