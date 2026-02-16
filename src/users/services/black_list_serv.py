from typing import List
from fastapi import HTTPException, status
from src.users.repositories.user_repository import UserRepository
from src.users.repositories.black_list_repo import BlackListRepo
from src.users.schemas.user.user_read import UserRead
from src.users.schemas.black_list.read import BlackListRead


class BlackListService:
    """Бизнес-логика для управления черным списком."""

    def __init__(
        self,
        blacklist_repository: BlackListRepo,
        user_repository: UserRepository,
    ):
        self.blacklist_repo = blacklist_repository
        self.user_repo = user_repository

    async def add_to_blacklist(self, user_id: int) -> None:
        """Добавить пользователя в черный список."""

        # 1. Проверяем, существует ли пользователь
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

        # 2. Проверяем, не находится ли пользователь уже в черном списке
        is_blocked = await self.blacklist_repo.is_blacklisted(user_id)
        if is_blocked:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь уже находится в черном списке",
            )

        # 3. Добавляем пользователя в черный список
        await self.blacklist_repo.add(user_id)

    async def remove_from_blacklist(self, user_id: int) -> None:
        """Удалить пользователя из черного списка."""
        deleted = await self.blacklist_repo.remove(user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден в черном списке"
            )

    async def get_all_blocked_users(self) -> List[UserRead]:
        """Получить список всех заблокированных пользователей."""
        users = await self.blacklist_repo.get_all_blacklisted_users()
        return [BlackListRead.model_validate(u) for u in users]

    async def check_user_blocked(self, user_id: int) -> bool:
        """Простая проверка статуса блокировки."""
        return await self.blacklist_repo.is_blacklisted(user_id)
