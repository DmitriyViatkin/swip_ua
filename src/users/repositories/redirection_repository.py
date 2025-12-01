from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from src.users.models.redirection import Redirections


class RedirectionRepository:
    """ Repository for Redirections model. """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, redir_id: int) -> Optional[Redirections]:
        stmt = select(Redirections).where(Redirections.id == redir_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Redirections]:
        stmt = select(Redirections)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_user(self, user_id: int) -> List[Redirections]:
        stmt = select(Redirections).where(Redirections.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, **data) -> Redirections:
        redirection = Redirections(**data)
        self.session.add(redirection)
        await self.session.commit()
        await self.session.refresh(redirection)
        return redirection

    async def update(self, redir_id: int, **data) -> Optional[Redirections]:
        stmt = (
            update(Redirections)
            .where(Redirections.id == redir_id)
            .values(**data)
            .returning(Redirections)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, redir_id: int) -> None:
        stmt = delete(Redirections).where(Redirections.id == redir_id)
        await self.session.execute(stmt)
        await self.session.commit()
