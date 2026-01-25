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

        # 2. Получаем все изображения галереи, отсортированные по позиции
        images_stmt = (
            select(GalleryImage)
            .where(GalleryImage.gallery_id == gallery_id)
            .order_by(GalleryImage.position)
        )

        images = (await session.execute(images_stmt)).scalars().all()

        if not images:
            return

        # Карты позиций пользователя
        order_map = {item.id: item.position for item in items}
        used_positions = set(order_map.values())

        # Картинки с пользовательскими позициями
        user_images = [img for img in images if img.id in order_map]
        user_images.sort(key=lambda img: order_map[img.id])

        # Картинки без указанных позиций
        other_images = [img for img in images if img.id not in order_map]

        # Функция для поиска свободной позиции, сдвигая вперёд при конфликтах
        def find_next_free_position(start_pos, used_pos_set):
            pos = start_pos
            while pos in used_pos_set:
                pos += 1
            return pos

        # Назначаем позиции пользовательским картинкам строго из order_map
        for img in user_images:
            img.position = order_map[img.id]


        # Чтобы избежать конфликта, теперь для остальных картинок назначаем позиции:
        # Если позиция у старой картинки конфликтует, сдвигаем вперёд до свободной
        occupied_positions = set(order_map.values())

        for img in other_images:
            new_pos = find_next_free_position(img.position, occupied_positions)
            img.position = new_pos
            img.is_main = False
            occupied_positions.add(new_pos)



        await session.flush()

