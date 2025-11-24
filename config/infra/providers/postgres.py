""" Dependency configuration for postgres. """

from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config.infra.config.settings import InfraSettings, infra_settings

class PostgresProvider(Provider):
    """ Provider class for postgres. """

    @provide(scope=Scope.APP)
    def provide_session_maker(self,infra_settings: InfraSettings) -> (
            async_sessionmaker)[AsyncSession]:
        """ Provide async session maker. """
        return async_sessionmaker(
            infra_settings.db.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )
    @provide(scope=Scope.REQUEST)
    async def provide_session(self,
        session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:

        """ Provide async session. """

        async with session_maker() as session:
            yield session