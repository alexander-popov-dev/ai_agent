from typing import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from database.redis.settings import RedisSettings, get_redis_settings


class BaseRedisProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> RedisSettings:
        return get_redis_settings()


class RedisDefaultDBProvider(BaseRedisProvider):
    component = "default"

    @provide(scope=Scope.APP)
    async def get_default_db(self, settings: RedisSettings) -> AsyncIterable[Redis]:
        client = Redis.from_url(url=settings.default_url, decode_responses=True)
        yield client
        await client.aclose()


class RedisCacheDBProvider(BaseRedisProvider):
    component = "cache"

    @provide(scope=Scope.APP)
    async def get_cache_db(self, settings: RedisSettings) -> AsyncIterable[Redis]:
        client = Redis.from_url(url=settings.cache_url, decode_responses=True)
        yield client
        await client.aclose()


class RedisFSMDBProvider(BaseRedisProvider):
    component = "fsm"

    @provide(scope=Scope.APP)
    @provide(scope=Scope.APP)
    async def get_fsm_db(self, settings: RedisSettings) -> AsyncIterable[Redis]:
        client = Redis.from_url(url=settings.bots_fsm_url, decode_responses=True)
        yield client
        await client.aclose()
