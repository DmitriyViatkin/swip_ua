from collections.abc import AsyncGenerator
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from config.infra.config.settings import InfraSettings

class PostgresProvider(Provider):

    # Session maker живе на рівні додатку
    @provide(scope=Scope.APP)
    def provide_session_maker(
        self,
        infra_settings: InfraSettings
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            infra_settings.db.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    # Сама сесія — в Scope.REQUEST
    @provide(scope=Scope.REQUEST)
    async def provide_session(
        self,
        session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session
