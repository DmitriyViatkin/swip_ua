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
        if not items:
            return

        # 1. Получаем gallery_id объявления
        gallery_id_stmt = (
            select(Gallery.id)
            .join(Advert, Advert.gallery_id == Gallery.id)
            .where(Advert.id == advert_id)
        )

        gallery_id = await session.scalar(gallery_id_stmt)

        if not gallery_id:
            raise ValueError("Gallery not found for advert")

        # 2. Загружаем все картинки галереи
        images_stmt = (
            select(GalleryImage)
            .where(GalleryImage.gallery_id == gallery_id)
            .order_by(GalleryImage.position)
        )

        images = (await session.execute(images_stmt)).scalars().all()

        if not images:
            return

        images_by_id = {img.id: img for img in images}

        # 3. Оставляем только валидные id
        order_map = {
            item.id: item.position
            for item in items
            if item.id in images_by_id
        }

        if not order_map:
            return

        # 4. Пользовательские картинки
        user_images = [images_by_id[iid] for iid in order_map]
        user_images.sort(key=lambda img: order_map[img.id])

        # 5. Остальные картинки
        other_images = [img for img in images if img.id not in order_map]

        # 6. Поиск свободной позиции
        def find_next_free_position(start: int, occupied: set[int]) -> int:
            pos = start
            while pos in occupied:
                pos += 1
            return pos

        # 7. Назначаем пользовательские позиции
        occupied_positions = set()

        for img in user_images:
            img.position = order_map[img.id]
            occupied_positions.add(img.position)

        # 8. Сдвигаем остальные картинки
        for img in other_images:
            new_pos = find_next_free_position(img.position, occupied_positions)
            img.position = new_pos
            img.is_main = False
            occupied_positions.add(new_pos)

        await session.flush()

