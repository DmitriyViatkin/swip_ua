""" Dependency configuration for redis. """
from typing import AsyncGenerator

from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from redis.asyncio import Redis
from config.infra.config.settings import InfraSettings, infra_settings

class RedisProvider(Provider):
    """ Provider class for Redis. """

    scope = Scope.APP

    @provide
    async  def provider_redis_client(self) -> AsyncGenerator[Redis, None]:
        """ Provide a Redis client (singleton for the application).

            Creates a connection pool on startup and closes it on shutdown.
        """
        redis = Redis.from_url(
            url=infra_settings.redis.url,
            password=infra_settings.redis.password,
            encodings="utf-8",
            decode_responses=True,
        )