from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.repositories.redirection_repository import RedirectionRepository
from src.users.services.redirection_service import RedirectionService


class RedirectionProvider(Provider):
    """DI provider for Redirection module."""
    repo = provide(
        RedirectionRepository,
        scope=Scope.REQUEST,
    )

    # Сервис получает repo
    service = provide(
        RedirectionService,
        scope=Scope.REQUEST
    )

