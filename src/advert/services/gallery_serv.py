from src.building.services.base import BaseService
from sqlalchemy import select
from src.advert.repositories.gallery_repo import GalleryRepository
from src.advert.models.gallery import Gallery,GalleryImage
from src.advert.models.advert import Advert
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.galery_order import GalleryOrder
from sqlalchemy.orm import selectinload

class GalleryService(BaseService[Gallery]):
    def __init__(self):
        super().__init__(GalleryRepository())

    from src.advert.models.gallery import Gallery, GalleryImage

    async def add_image_to_advert(
            self,
            session: AsyncSession,
            advert_id: int,
            image_data: dict,
    ):
        # Получаем или создаём галерею для объявления
        result = await session.execute(
            select(Gallery).where(Gallery.advert_id == advert_id)
        )
        gallery = result.scalar_one_or_none()

        if not gallery:
            gallery = Gallery(advert_id=advert_id)
            session.add(gallery)
            await session.commit()
            await session.refresh(gallery)

        # Вычисляем позицию для нового изображения (нужно метод в репозитории)
        position = await self.repository.get_next_position(
            session=session,
            gallery_id=gallery.id,
        )

        # Создаём новую запись изображения
        gallery_image = GalleryImage(
            gallery_id=gallery.id,
            image=image_data["filename"],
            position=position,
            is_main=image_data.get("is_main", False),
        )

        session.add(gallery_image)
        await session.commit()
        await session.refresh(gallery_image)

        return gallery_image

    async def reorder_for_house(self, session: AsyncSession, house_id: int,
                                items:list[GalleryOrder] ):
        async with session.begin():
            await self.repository.bulk_reorder(
                session=session,
                items=items,
                house_id=house_id
            )
    async def reorder_for_advert(self, session:AsyncSession,
                                 advert_id:int,items= list[GalleryOrder], ):
        async with session.begin():
            await self.repository.bulk_reorder(
                session=session,
                items=items,
                advert_id=advert_id

        )

    async def get_gallery_by_advert(self, session: AsyncSession, advert_id: int):
        result = await session.execute(
            select(Gallery)
            .options(selectinload(Gallery.images))  # <- предзагрузка изображений
            .join(Advert, Gallery.id == Advert.gallery_id)
            .where(Advert.id == advert_id)
        )
        return result.scalar_one_or_none()