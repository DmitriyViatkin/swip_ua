from src.building.repositories.base import BaseRepository

from sqlalchemy.orm import selectinload


from sqlalchemy import update, case, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.advert.models.gallery import GalleryImage, Gallery
from src.advert.models.advert import Advert
from src.advert.schemas.gallery_order_sch import GalleryOrder

class GalleryImageRepository(BaseRepository[GalleryImage]):
    def __init__(self):
        super().__init__(GalleryImage)

    async def get_by_id_with_gallery(
        self,
        session: AsyncSession,
        image_id: int,
    ) -> GalleryImage | None:
        stmt = (
            select(GalleryImage)
            .where(GalleryImage.id == image_id)
            .options(selectinload(GalleryImage.gallery))
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_gallery_id(
        self,
        session: AsyncSession,
        gallery_id: int,
    ):
        stmt = (
            select(GalleryImage)
            .where(GalleryImage.gallery_id == gallery_id)
            .order_by(GalleryImage.position)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def bulk_reorder(
        self,
        session: AsyncSession,
        items: list[GalleryOrder],
    ):
        if not items:
            return

        stmt = (
            update(GalleryImage)
            .where(GalleryImage.id.in_([i.id for i in items]))
            .values(
                position=case(
                    {i.id: i.position for i in items},
                    value=GalleryImage.id,
                )
            )
        )

        await session.execute(stmt)
