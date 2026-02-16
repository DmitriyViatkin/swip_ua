from redis.asyncio import Redis
from config.config.settings import InfraSettings
from config.infra.config.settings import redis_settings

settings = InfraSettings()
redis_settings = settings.redis

redis_client = Redis.from_url(
    redis_settings.url,
    encoding="utf-8",
    decode_responses = True

)


