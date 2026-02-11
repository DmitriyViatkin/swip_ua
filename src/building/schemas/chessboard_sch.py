# src/building/schemas/chessboard_sch.py

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class ChessboardCell(BaseModel):
    flat_id: Optional[int] = None
    price: Optional[Decimal] = None
    area: Optional[float] = None
    image: Optional[str] = None


class ChessboardRow(BaseModel):
    floor: int
    risers: dict[int, ChessboardCell]