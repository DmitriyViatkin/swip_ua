from .base import BaseRepository
from src.building.models.house import House
from src.advert.models.gallery import Gallery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

class HouseRepository(BaseRepository[House]):
    def __init__(self):
        super().__init__(House)

    async def get_by_user_id(self, session: AsyncSession, user_id: int):
        query = select(House).where(House.user_id == user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id_and_user(self, session: AsyncSession, house_id: int, user_id: int) -> House | None:
        result = await session.execute(
            select(House).where(House.id == house_id, House.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, session: AsyncSession, house_id: int) -> House | None:
        stmt = (
            select(House)
            .where(House.id == house_id)
            .options(
                selectinload(House.infrastructure),
                selectinload(House.registration_and_payment),
                selectinload(House.documents),
                selectinload(House.news),
                selectinload(House.gallery).selectinload(Gallery.images),
            )
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()