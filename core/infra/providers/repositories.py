
from collections.abc import AsyncIterable

'''from dishka import Provider, Scope, provide, FromDishka
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.infra.config.settings import InfraSettings, infra_settings

class RepositoriesProvider(Provider):
    """ Provider class for Repositories. """

    @provide(scope=Scope.REQUEST)
    def api_key_repository(self, session: FromDishka[AsyncSession]) -> ApiKeyRepository:
        """ Provide an instance of the ApiKeyRepository"""
        return ApiKeyRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def deal_repository(self, session: FromDishka[AsyncSession]) -> DeelRepository:
        """ Provide an instance of the DealRepository. """
        return DealRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def order_repository(self, session: FromDishka[AsyncSession]) -> OrderRepository:
        """ Provide an instance of the OrderRepository. """
        return OrderRepository(session=session)'''