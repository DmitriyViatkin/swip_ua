# src/advert/repositories/advert_repo.py




from .advert_base_repo import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from ..models.advert import Advert
from typing import Type
from sqlalchemy.orm import selectinload

class AdvertRepository(BaseRepository[Advert]):
    model = Advert

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_build(self, build_id: int) -> list[Advert]:
        stmt = select(Advert).where(Advert.build_id == build_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def exists(self, advert_id: int) -> bool:
        stmt = select(Advert.id).where(Advert.id == advert_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def set_gallery(self, advert_id: int, gallery_id: int):
        stmt = (
            update(Advert)
            .where(Advert.id == advert_id)
            .values(gallery_id=gallery_id)
        )
        await self.session.execute(stmt)
        await self.session.flush()

    async def get_by_id_with_gallery(self, advert_id: int) -> Advert | None:
        stmt = select(Advert).where(Advert.id == advert_id).options(
            selectinload(Advert.gallery)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
