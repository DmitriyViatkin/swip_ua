from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from src.users.models import Subscription   # путь поправь под себя


class SubscriptionRepository:
    """Repository for Subscription model."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, subscription_id: int) -> Optional[Subscription]:
        stmt = select(Subscription).where(Subscription.id == subscription_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Optional[Subscription]:
        stmt = select(Subscription).where(Subscription.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Subscription]:
        stmt = select(Subscription)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, **data) -> Subscription:
        obj = Subscription(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, subscription_id: int, **data) -> Optional[Subscription]:
        stmt = (
            update(Subscription)
            .where(Subscription.id == subscription_id)
            .values(**data)
            .returning(Subscription)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, subscription_id: int) -> None:
        stmt = delete(Subscription).where(Subscription.id == subscription_id)
        await self.session.execute(stmt)
        await self.session.commit()