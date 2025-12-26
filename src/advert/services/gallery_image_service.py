from src.advert.models.gallery import GalleryImage
from sqlalchemy.ext.asyncio import AsyncSession

class GalleryImageService:
    async def create(self, session: AsyncSession, data: dict) -> GalleryImage:
        if not data.get("gallery_id"):
            raise ValueError("gallery_id is required for GalleryImage")

        image = GalleryImage(**data)
        session.add(image)
        await session.commit()
        await session.refresh(image)
        return image