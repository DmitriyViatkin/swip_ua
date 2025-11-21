from typing import List, Optional
from src.users.repositories.user_repository import UserRepository
from src.users.schemas.user.user_create import UserCreateSchema
from src.users.schemas.user.user_update import UserUpdate
from src.users.schemas.user.user_read import UserRead
from src.enums import UserRole


class UserService:
    """ Business logic for User. """

    def __init__ (self, repo: UserRepository) :
        self.repo = repo

    async def get_user(self, user_id: int) ->Optional[UserRead]:
        user = await self.repo.get_by_id(user_id)
        if not user:
            return None
        return UserRead.model_validate(user)

    async def get_all_users(self)->List[UserRead]:
        users = await self.repo.get_all()
        return [ UserRead.model_validate(u) for u in users]

    async def create_user (self, data: UserCreateSchema)-> UserRead:
        user = await self.repo.create(**data.model_dump())
        return UserRead.model_validate(user)

    async def update_user (self, user_id: int, data: UserUpdate) -> Optional[
        UserRead]:

        user = await self.repo.update(user_id, **data.model_dump(exclude_unset=True))
        if not user:
            return None
        return UserRead.model_validate(user)

    async def delete_user(self, user_id: int) -> None:
        await self.repo.delete(user_id)

    async def get_user_by_role (self, role: UserRole):
        user = await self.repo.get_by_role(role)
        return [UserRead.model_validate(u) for u in users]