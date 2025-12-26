from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, TypeVar
from src.building.repositories.base import BaseRepository

Model = TypeVar("Model")


class BaseService(Generic[Model]):
    def __init__(self, repository: BaseRepository[Model]):
        self.repository = repository

    async def get_all(self, session: AsyncSession):
        return await self.repository.get_all(session)

    async def get_by_id(self, session: AsyncSession, pk: int):
        return await self.repository.get_by_id(session, pk)

    async def create(self, session: AsyncSession, data: dict):
        obj = await self.repository.create(session, data)
        await session.commit()
        return obj

    async def update(self, session: AsyncSession, pk: int, data: dict):
        obj = await self.repository.get_by_id(session, pk)
        if not obj:
            return None

        obj = await self.repository.update(session, obj, data)
        await session.commit()
        return obj

    async def delete(self, session: AsyncSession, pk: int):
        obj = await self.repository.get_by_id(session, pk)
        if not obj:
            return None

        await self.repository.delete(session, obj)
        await session.commit()
        return True
