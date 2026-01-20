from src.building.repositories.base import BaseRepository
from src.advert.models.promotion import Promotion
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class PromotionRepository(BaseRepository[Promotion]):
    def __init__(self):
        super().__init__(Promotion)

    async def get_by_advert_id(self, session: AsyncSession, advert_id: int):
        stmt = select(self.model).where(self.model.advert_id == advert_id).order_by(self.model.id.desc())
        result = await session.execute(stmt)
        # Берем первый из списка найденных
        return result.scalars().first()