from functools import cache

from redis.asyncio import Redis

from src.database.redis.settings import get_redis_settings


class RedisFactory:
    def __init__(self):
        self._settings = get_redis_settings()

    @cache
    def create_default_db_client(self) -> Redis:
        return Redis.from_url(url=self._settings.default_url, decode_responses=True)

    @cache
    def create_cache_db_client(self) -> Redis:
        return Redis.from_url(url=self._settings.cache_url, decode_responses=True)

    @cache
    def create_fsm_db_client(self) -> Redis:
        return Redis.from_url(url=self._settings.bots_fsm_url, decode_responses=True)
