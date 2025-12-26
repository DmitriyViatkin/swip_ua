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
                items: list[GalleryOrder],
                house_id: int
        ):
            """
            Меняет порядок картинок в рамках одного дома
            """

            for item in items:
                await session.execute(
                    update(Gallery)
                    .where(
                        Gallery.id == item.id,
                        Gallery.house_id == house_id
                    )
                    .values(position=item.position)
                )

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