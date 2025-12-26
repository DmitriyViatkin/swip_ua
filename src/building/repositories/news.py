

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.building.models.news import News
from src.building.repositories.base import BaseRepository


class NewsRepository(BaseRepository[News]):
    def __init__(self):
        super().__init__(News)

    async def get_last_by_house(
        self,
        session: AsyncSession,
        house_id: int,
        limit: int = 5,
    ):
        stmt = (
            select(News)
            .where(News.house_id == house_id)
            .order_by(News.id.desc())
            .limit(limit)
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_all_by_house(
            self,
            session: AsyncSession,
            house_id: int,
    ) -> list[News]:
        stmt = select(News).where(News.house_id == house_id)
        result = await session.execute(stmt)
        return result.scalars().all()
