from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.repositories.favoriete_repo import FavoritesRepository
from src.users.schemas.favorite.favorite_create_sch import FavoriteCreate
from src.users.models.favorite import Favorite


class FavoritesService:
    def __init__(self, session: AsyncSession):
        self.repository = FavoritesRepository(session)

    async def add_to_favorites(self, user_id: int, favorite_data: FavoriteCreate) -> Optional[Favorite]:
        """
        Логіка додавання оголошення в обране.
        """
        # Викликаємо репозиторій
        favorite = await self.repository.create_favorites(user_id, favorite_data)

        if not favorite:


            return None

        return favorite

    async def get_my_favorites(self, user_id: int) -> List[Favorite]:
        """
        Отримання списку всіх обраних оголошень користувача.
        """
        return await self.repository.get_user_favorites(user_id)

    async def remove_from_favorites(self, user_id: int, advert_id: int) -> bool:
        """
        Логіка видалення оголошення з обраного.
        Повертає True, якщо видалення успішне, і False, якщо запису не було.
        """
        return await self.repository.delete_favorite(user_id, advert_id)