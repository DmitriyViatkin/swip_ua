

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, exists
from sqlalchemy.orm import selectinload
from src.users.models import User, BlackList

class BlackListRepo:
    """Repository for BlackList management."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user_id: int) -> BlackList:
        """Добавить пользователя в черный список."""
        black_list_item = BlackList(user_id=user_id)
        self.session.add(black_list_item)
        await self.session.commit()
        await self.session.refresh(black_list_item)
        return black_list_item

    async def remove(self, user_id: int) -> bool:
        """Удалить пользователя из черного списка."""
        stmt = delete(BlackList).where(BlackList.user_id == user_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def is_blacklisted(self, user_id: int) -> bool:
        """Проверить, находится ли пользователь в черном списке."""
        stmt = select(exists().where(BlackList.user_id == user_id))
        result = await self.session.execute(stmt)
        return result.scalar_one()  # scalar_one() вернет True/False

    async def get_all_blacklisted_users(self) -> List[User]:
        """Получить список всех пользователей, которые находятся в черном списке."""
        stmt = (
            select(User)
            .join(BlackList, User.id == BlackList.user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()  # убран лишний list() и .all() внутри list()

    async def get_by_user_id(self, user_id: int) -> Optional[BlackList]:
        """Найти запись в черном списке по ID пользователя."""
        stmt = select(BlackList).where(BlackList.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
