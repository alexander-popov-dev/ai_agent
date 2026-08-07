from functools import cache
from typing import ClassVar

from pydantic import Field

from src.settings import BaseProjectSettings


class RedisSettings(BaseProjectSettings):
    """Redis connection settings.

    A single Redis instance hosts several logical databases (indexes 0–15).
    Each application role is pinned to a fixed index so keyspaces between
    cache, bots FSM and future roles never collide.
    """

    redis_host: str = Field(alias="REDIS_HOST")
    redis_pass: str = Field(alias="REDIS_PASS")
    redis_port: str = Field(alias="REDIS_PORT")

    # Role → DB index mapping. Declared as ClassVar so pydantic treats
    # them as class-level constants rather than env-driven fields.
    # These values are part of the application contract and must stay
    # identical across machines.
    REDIS_DB_DEFAULT: ClassVar[int] = 10
    REDIS_DB_CACHE: ClassVar[int] = 11
    REDIS_DB_BOTS_FSM: ClassVar[int] = 12

    def _url(self, db: int) -> str:
        """Build a Redis URL for the given logical database index.

        Private helper. Callers should use the semantic properties below
        so the DB index is never chosen ad-hoc at the call site.
        """
        return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/{db}"

    @property
    def default_url(self) -> str:
        """URL for the default DB (used for healthcheck pings)."""
        return self._url(db=self.REDIS_DB_DEFAULT)

    @property
    def cache_url(self) -> str:
        """URL for the backend cache database."""
        return self._url(db=self.REDIS_DB_CACHE)

    @property
    def bots_fsm_url(self) -> str:
        """URL for aiogram FSM storage used by the Telegram bots."""
        return self._url(db=self.REDIS_DB_BOTS_FSM)


# noinspection PyArgumentList
@cache
def get_redis_settings() -> RedisSettings:
    """Return the singleton RedisSettings instance."""
    return RedisSettings()  # pyright: ignore[reportCallIssue]
