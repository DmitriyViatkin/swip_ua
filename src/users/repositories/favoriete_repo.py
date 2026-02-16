
from sqlalchemy import select, or_, and_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.models.favorite import Favorite
from src.users.schemas.favorite.favorite_create_sch import FavoriteCreate
from typing import  Optional, List

class FavoritesRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_favorites(self, user_id: int, favorite_data: FavoriteCreate)->Optional[Favorite]:
        """
            Додає оголошення до списку обраного.
            Ми передаємо user_id окремо (зазвичай з токена),
            а advert_id беремо зі схеми.
        """
        db_favorite = Favorite(user_id = user_id, advert_id= favorite_data.advert_id)
        self.session.add(db_favorite)
        try:
            await self.session.commit()
            await self.session.refresh(db_favorite)
            return db_favorite
        except Exception:
            await self.session.rollback()
            return None

    async def get_user_favorites(self, user_id: int):

        """Отримує всі обрані оголошення користувача."""

        query = select(Favorite).where(Favorite.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete_favorite(self, user_id: int , advert_id: int)-> bool:
        """Видаляє оголошення з обраного."""
        query = delete(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.advert_id == advert_id
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0
