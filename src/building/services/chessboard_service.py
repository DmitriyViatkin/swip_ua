# src/building/services/chessboard.py
from src.building.repositories.chessboard_repository import ChessboardRepository



from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.building.models.flat import Flat
from src.building.models.floor import Floor
from src.building.models.riser import Riser
from src.building.models.section import Section
from src.building.schemas.chessboard_sch import ChessboardCell, ChessboardRow
from collections import defaultdict

class ChessboardService:
    def __init__(self):
        self.repo = ChessboardRepository()

    async def get_section_chessboard(
        self,
        session: AsyncSession,
        house_id: int,
        section_id: int
    ) -> list[ChessboardRow]:
        """
        Возвращает шахматку для указанного дома и секции
        """
        flats_data = await self.repo.get_by_section_and_house(
            session=session,
            house_id=house_id,
            section_id=section_id
        )

        # Группируем по этажам
        chess_dict = defaultdict(dict)  # floor_name -> {riser_id: ChessboardCell}
        for flat in flats_data:
            chess_dict[flat['floor']][flat['riser_id']] = ChessboardCell(
                flat_id=flat['flat_id'],
                price=flat['price'],
                area=flat['area'],
            )

        # Определяем все riser_id для пустых ячеек
        all_risers = sorted({flat['riser_id'] for flat in flats_data})

        rows = []
        for floor_name, risers_cells in sorted(chess_dict.items(), key=lambda x: -int(x[0])):
            row_cells = {riser_id: risers_cells.get(riser_id, ChessboardCell()) for riser_id in all_risers}
            rows.append(ChessboardRow(floor=floor_name, risers=row_cells))

        return rows


    async def get_all_chessboards(self, session: AsyncSession) -> list[ChessboardRow]:
        """
        Возвращает шахматки для всех домов, секций, этажей и стояков
        """
        # получаем flats с этажами и стояками, присоединяя Section и Corps для фильтрации по дому
        result = await session.execute(
            select(
                Flat.id, Flat.price, Flat.area, Flat.image,
                Floor.name.label("floor_name"),
                Floor.section_id,
                Section.corps_id,
                Riser.id.label("riser_id")
            )
            .join(Floor, Flat.floor_id == Floor.id)
            .join(Riser, Flat.riser_id == Riser.id)
            .join(Section, Floor.section_id == Section.id)
            .order_by(Section.corps_id, Floor.section_id, Floor.name.desc(), Riser.id.asc())
        )

        flats_data = result.all()

        # Группируем по corps -> section -> floor -> riser
        chess_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        for flat_id, price, area, image, floor_name, section_id, corps_id, riser_id in flats_data:
            chess_dict[corps_id][section_id][floor_name][riser_id] = ChessboardCell(
                flat_id=flat_id, price=price, area=area, image=image
            )

        rows = []
        for corps_id, sections in chess_dict.items():
            for section_id, floors in sections.items():
                # Получаем все riser_id для этой секции
                risers_result = await session.execute(
                    select(Riser.id).where(Riser.section_id == section_id).order_by(Riser.id.asc())
                )
                all_risers = [r[0] for r in risers_result.all()]

                for floor_name, risers_cells in sorted(floors.items(), key=lambda x: -x[0]):
                    row_cells = {riser_id: risers_cells.get(riser_id, ChessboardCell()) for riser_id in all_risers}
                    rows.append(ChessboardRow(floor=floor_name, risers=row_cells))

        return rows


    async def add_flat_to_chessboard(self, session: AsyncSession, flat_data: dict) -> Flat:
        """
        Добавление нового флата в шахматку
        """
        new_flat = Flat(**flat_data)
        session.add(new_flat)
        await session.flush()
        await session.commit()
        return new_flat