from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import TypeVar, Generic

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, pk: int):
        result = await self.session.execute(
            select(self.model).where(self.model.id == pk)
        )
        return result.scalar_one_or_none()

    async def create(self, obj_data: dict):
        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update(self, db_obj, obj_data: dict):
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        await self.session.flush()
        return db_obj

    async def delete(self, db_obj):
        await self.session.delete(db_obj)
        await self.session.flush()