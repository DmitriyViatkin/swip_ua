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
            advert_id: int,
            items: list[GalleryOrder],
    ):
        # 1. Получаем gallery_id
        gallery_id_stmt = (
            select(Gallery.id)
            .join(Advert, Advert.gallery_id == Gallery.id)
            .where(Advert.id == advert_id)
        )

        gallery_id = await session.scalar(gallery_id_stmt)

        if not gallery_id:
            raise ValueError("Gallery not found for advert")

        # 2. Получаем ВСЕ изображения галереи в текущем порядке
        images_stmt = (
            select(GalleryImage)
            .where(GalleryImage.gallery_id == gallery_id)
            .order_by(GalleryImage.position)
        )

        images = (await session.execute(images_stmt)).scalars().all()

        if not images:
            return

        # 3. Формируем новый порядок
        order_map = {item.id: item.position for item in items}

        # сортируем:
        # - те, что пришли — по position
        # - остальные — в конец, сохраняя относительный порядок
        images.sort(
            key=lambda img: (
                0 if img.id in order_map else 1,
                order_map.get(img.id, img.position),
            )
        )

        # 4. Пересчитываем позиции с 0
        for index, image in enumerate(images):
            image.position = index
            image.is_main = index == 0

        await session.flush()

