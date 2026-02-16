from src.building.services.base import BaseService
from sqlalchemy import select
from src.advert.repositories.gallery_repo import GalleryRepository
from src.advert.models.gallery import Gallery,GalleryImage
from src.advert.models.advert import Advert
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.galery_order import GalleryOrder
from sqlalchemy.orm import selectinload

from sqlalchemy import select, func

class GalleryService(BaseService[Gallery]):
    def __init__(self):
        super().__init__(GalleryRepository())

    async def get_next_position(
            self,
            session: AsyncSession,
            gallery_id: int,
    ) -> int:
        stmt = (
            select(func.coalesce(func.max(GalleryImage.position), 0))
            .where(GalleryImage.gallery_id == gallery_id)
        )
        result = await session.execute(stmt)
        return result.scalar_one() + 1

    async def add_image_to_advert(
            self,
            session: AsyncSession,
            advert_id: int,
            image_data: dict,
    ):
        advert = await session.get(Advert, advert_id, options=[selectinload(Advert.gallery)])
        if not advert:
            raise Exception(f"Advert with id {advert_id} not found")

        gallery = advert.gallery
        if not gallery:
            gallery = Gallery()
            session.add(gallery)
            await session.flush()
            advert.gallery_id = gallery.id

        position = await self.get_next_position(session, gallery.id)

        gallery_image = GalleryImage(
            gallery_id=gallery.id,
            image=image_data["filename"],
            position=position,
            is_main=image_data.get("is_main", False),
        )
        session.add(gallery_image)
        await session.flush()
        return gallery_image


    async def reorder_for_house(self, session: AsyncSession, house_id: int,
                                items:list[GalleryOrder] ):

            await self.repository.bulk_reorder(
                session=session,
                items=items,
                house_id=house_id
            )

    async def reorder_for_advert(self, session: AsyncSession, advert_id: int, items: list[GalleryOrder]):

            await self.repository.bulk_reorder(session=session, items=items)

    async def get_gallery_by_advert(self, session: AsyncSession, advert_id: int):
        result = await session.execute(
            select(Gallery)
            .options(selectinload(Gallery.images))
            .join(Advert, Gallery.id == Advert.gallery_id)
            .where(Advert.id == advert_id)
        )
        return result.scalar_one_or_none()