from abc import ABC, abstractmethod

from src.core.logging.mixin import LoggedMixin
from src.pipelines.reels.session.config import ReelsSessionConfig


class BaseRepository(ABC, LoggedMixin):
    __log_layer__ = "repository"

    @abstractmethod
    async def get(self, user_id: int) -> ReelsSessionConfig:
        ...

    @abstractmethod
    async def save(self, user_id: int, schema: ReelsSessionConfig) -> None:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        ...
