from .base import BaseRepository
from src.building.models.infrastructure import Infrastructure
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class InfrastructureRepository(BaseRepository[Infrastructure]):
    def __init__(self):
        super().__init__(Infrastructure)

    async def get_by_house_id(
            self,
            session: AsyncSession,
            house_id: int,
    ) -> Infrastructure | None:
        result = await session.execute(
            select(Infrastructure).where(
                Infrastructure.house_id == house_id
            )
        )
        return result.scalars().first()