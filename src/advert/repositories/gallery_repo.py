from src.building.repositories.base import BaseRepository
from src.advert.models.gallery import Gallery
from ..schemas.galery_order import GalleryOrder
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, func


from src.advert.models.gallery import Gallery

class GalleryRepository(BaseRepository[Gallery]):
    def __init__(self):
        super().__init__(Gallery)

    async def bulk_reorder(
        self,
        session: AsyncSession,
        house_id: int,
        items: list[GalleryOrder],
    ):
        """
        Меняет порядок галерей в рамках одного дома
        Логика полностью аналогична GalleryImageRepository.bulk_reorder
        """

        # 1. Получаем все галереи дома, отсортированные по позиции
        stmt = (
            select(Gallery)
            .where(Gallery.house_id == house_id)
            .order_by(Gallery.position)
        )

        galleries = (await session.execute(stmt)).scalars().all()

        if not galleries:
            return

        # 2. Карта пользовательских позиций
        order_map = {item.id: item.position for item in items}
        used_positions = set(order_map.values())

        # 3. Галереи с пользовательскими позициями
        user_galleries = [g for g in galleries if g.id in order_map]
        user_galleries.sort(key=lambda g: order_map[g.id])

        # 4. Галереи без указанных позиций
        other_galleries = [g for g in galleries if g.id not in order_map]

        # 5. Поиск свободной позиции
        def find_next_free_position(start_pos: int, occupied: set[int]) -> int:
            pos = start_pos
            while pos in occupied:
                pos += 1
            return pos

        # 6. Назначаем позиции пользовательским галереям
        for gallery in user_galleries:
            gallery.position = order_map[gallery.id]

        occupied_positions = set(order_map.values())

        # 7. Остальные галереи аккуратно сдвигаем
        for gallery in other_galleries:
            new_pos = find_next_free_position(gallery.position, occupied_positions)
            gallery.position = new_pos
            occupied_positions.add(new_pos)

        await session.flush()

    async def get_next_position(
        self,
        session: AsyncSession,
        house_id: int,
    ) -> int:
        stmt = (
            select(func.coalesce(func.max(Gallery.position), 0))
            .where(Gallery.house_id == house_id)
        )

        result = await session.execute(stmt)
        max_position = result.scalar_one()

        return max_position + 1