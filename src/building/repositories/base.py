from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Type, TypeVar, Generic

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model


    async def get_all(self, session: AsyncSession):
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, session: AsyncSession, pk: int):
        result = await session.execute(
            select(self.model).where(self.model.id == pk)
        )
        return result.scalars().first()

    async def create(self, session: AsyncSession, obj_data: dict):
        obj = self.model(**obj_data)
        session.add(obj)
        await session.flush()
        return obj

    async def update(self, session: AsyncSession, db_obj, obj_data: dict):
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        await session.flush()
        return db_obj

    async def delete(self, session: AsyncSession, db_obj):
        await session.delete(db_obj)
        await session.flush()
