from src.advert.models.gallery import GalleryImage, Gallery
from src.advert.models.advert import Advert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.advert.repositories.gallery_image_repo import GalleryImageRepository
from src.building.services.base import BaseService
from src.advert.schemas.gallery_order_sch import  GalleryOrder

class GalleryImageService(BaseService[GalleryImage]):
        def __init__(self, session: AsyncSession):
            super().__init__(GalleryImageRepository())

        async def create(self, session: AsyncSession, data: dict) -> GalleryImage:
            if not data.get("gallery_id"):
                raise ValueError("gallery_id is required for GalleryImage")

            image = GalleryImage(**data)
            session.add(image)
            await session.commit()
            await session.refresh(image)
            return image

        async def get_by_gallery_id(self, session:AsyncSession, gallery_id:int):
            return await self.repository.get_by_gallery_id(session, gallery_id)

        async def get_with_gallery(
                self,
                session: AsyncSession,
                image_id: int,
        ) -> GalleryImage | None:
            return await self.repository.get_by_id_with_gallery(session, image_id)

        async def reorder_for_advert(
                self,
                session: AsyncSession,
                advert_id: int,
                items: list[GalleryOrder],
        ):
            await self.repository.bulk_reorder(
                session=session,
                advert_id=advert_id,
                items=items,
            )

        async def get_advert_id_by_image_id(
                self,
                session: AsyncSession,
                image_id: int,
        ) -> int | None:
            stmt = (
                select(Advert.id)
                .join(Gallery, Advert.gallery_id == Gallery.id)
                .join(GalleryImage, GalleryImage.gallery_id == Gallery.id)
                .where(GalleryImage.id == image_id)
            )

            result = await session.execute(stmt)
            return result.scalar_one_or_none()