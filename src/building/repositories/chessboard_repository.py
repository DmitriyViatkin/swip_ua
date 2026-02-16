# src/building/repositories/chessboard.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.building.models.flat import Flat
from src.building.models.floor import Floor
from src.building.models.section import Section
from src.building.models.corps import Corps
from src.building.models.house import House
from src.building.models.riser import Riser


class ChessboardRepository:

    async def get_by_section_and_house(
        self,
        session: AsyncSession,
        house_id: int,
        section_id: int,
    ):
        """
        Возвращает шахматку для конкретного дома и секции
        """
        stmt = (
            select(
                Flat.id.label("flat_id"),
                Floor.name.label("floor"),
                Riser.name.label("riser"),
                Flat.price,
                Flat.area,
                Flat.floor_id,
                Flat.riser_id,
                Section.id.label("section_id"),
                Corps.id.label("corps_id"),
                House.id.label("house_id"),
            )
            .join(Floor, Floor.id == Flat.floor_id)
            .join(Riser, Riser.id == Flat.riser_id)
            .join(Section, Section.id == Floor.section_id)
            .join(Corps, Corps.id == Section.corps_id)
            .join(House, House.id == Corps.house_id)
            .where(
                House.id == house_id,
                Section.id == section_id
            )
            .order_by(Floor.name.desc(), Riser.name.asc())
        )

        result = await session.execute(stmt)
        return result.mappings().all()


    async def get_full_chessboards(self, session: AsyncSession):
        """
        Возвращает все шахматки по всем домам и секциям
        """
        stmt = (
            select(
                Flat.id.label("flat_id"),
                Floor.name.label("floor"),
                Riser.name.label("riser"),
                Flat.price,
                Flat.area,
                Flat.floor_id,
                Flat.riser_id,
                Section.id.label("section_id"),
                Corps.id.label("corps_id"),
                House.id.label("house_id"),
            )
            .join(Floor, Floor.id == Flat.floor_id)
            .join(Riser, Riser.id == Flat.riser_id)
            .join(Section, Section.id == Floor.section_id)
            .join(Corps, Corps.id == Section.corps_id)
            .join(House, House.id == Corps.house_id)
            .order_by(House.id, Section.id, Floor.name.desc(), Riser.name.asc())
        )

        result = await session.execute(stmt)
        return result.mappings().all()
