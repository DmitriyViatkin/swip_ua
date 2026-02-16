""" Dependency configuration for redis. """
from dishka import Provider, provide, Scope
from redis.asyncio import Redis
from typing import AsyncGenerator
from config.config.settings import InfraSettings

infra_settings = InfraSettings()

class RedisProvider(Provider):

    scope = Scope.APP

    @provide
    async def provider_redis_client(self) -> AsyncGenerator[Redis, None]:
        redis = Redis.from_url(
            url=infra_settings.redis.url,
            encoding="utf-8",
            decode_responses=True,
        )

        yield redis


        await redis.close()