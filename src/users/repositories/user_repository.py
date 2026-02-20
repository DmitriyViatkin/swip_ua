from typing import Optional, List

from mypy.stubgen import is_blacklisted_path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy import select, update, delete, or_
from src.users.models import User
from src.enums import UserRole
from sqlalchemy.orm import selectinload

class UserRepository:
    """ Repository for User model. """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = (
            select(User)
            .options(
                selectinload(User.agent),
                # Завантажуємо клієнтів ТА їхні підписки одним махом
                selectinload(User.clients).selectinload(User.subscription),
                # Також завантажуємо клієнтів для цих клієнтів (якщо це передбачено схемою UserRead)
                selectinload(User.clients).selectinload(User.clients),
                selectinload(User.subscription),
                selectinload(User.client_notifications),
                selectinload(User.redirections),
            )
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, role: Optional[str] = None) -> List[User]:
        stmt = (
            select(User)
            .options(
                selectinload(User.agent),
                selectinload(User.clients),
                selectinload(User.subscription),
                selectinload(User.client_notifications),
                selectinload(User.redirections),
            )
        )

        if role:
            stmt = stmt.where(User.role == role)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).options(
            selectinload(User.agent),
            selectinload(User.clients),
            selectinload(User.subscription),
            selectinload(User.client_notifications),
            selectinload(User.redirections),
        ).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_role(self, role: UserRole) -> List[User]:
        stmt = select(User).where(User.role == role)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, **data) -> User:
        user = User(**data)
        self.session.add(user)
        await self.session.flush()
        print(f"User created: {user}")
        return user

    async def update(self, user_id: int, **data) -> Optional[User]:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**data)
        )
        await self.session.execute(stmt)
        await self.session.commit()

        return await self.get_by_id(user_id)

    async def delete(self, user_id: int) -> None:
        stmt = delete(User).where(User.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_by_email_or_phone(self, login: str) -> Optional[User]:
        stmt = (
            select(User)
            .options(
                selectinload(User.agent),  # ← ОБЯЗАТЕЛЬНО
                selectinload(User.subscription),
                selectinload(User.agent),
                selectinload(User.client_notifications),
                selectinload(User.redirections),
            )
            .where((User.email == login) | (User.phone == login))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_blocked_user(self):

        stmt = (select(User).where(User.is_blacklisted == True))
        result = await self.session.execute(stmt)

        return result.scalars().all()


    async def update_password(self, user_id: int, new_hashed_password: str) -> Optional[User]:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(password=new_hashed_password)
        )
        await self.session.execute(stmt)
        await self.session.commit()

        return await self.get_by_id(user_id)

    async def update_photo(self, user_id: int, filename: str) -> Optional[User]:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(photo=filename)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_by_id(user_id)

    async def verified_email(self, user_id:int)->Optional[User]:
        """ Marks the user email as verified. """
        stmt=(update(User).where(User.id == user_id).values(is_email_verified=True)
              )
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_by_id(user_id)

    async def is_email_verified(self, user_id: int) -> bool:
        """Checks if the user's email is verified."""
        stmt = (
            select(User.is_email_verified)
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar() or False

    async def blacked_user (self,user_id:int)-> bool:

        """ Blocked User """
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(is_blacklisted=True)
            .returning(User.is_blacklisted)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()


        updated_status = result.scalar_one_or_none()


        return updated_status if updated_status is not None else False

    async def deblacked_user(self, user_id: int) -> bool:
        """ Blocked User """
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(is_blacklisted=False)
            .returning(User.is_blacklisted)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        updated_status = result.scalar_one_or_none()

        return updated_status if updated_status is not None else False