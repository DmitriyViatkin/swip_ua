from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.repositories.user_repository import UserRepository
from src.users.services.user_service import UserService


class UserProvider(Provider):
    """DI provider for user module."""

    scope = Scope.REQUEST

    @provide
    def user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide
    def user_service(self, user_repository: UserRepository) -> UserService:
        return UserService(user_repository)