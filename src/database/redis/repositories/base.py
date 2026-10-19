from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.core.logging.mixin import LoggedMixin


class BaseRepository[T: BaseModel](ABC, LoggedMixin):
    __log_layer__ = "repository"

    @abstractmethod
    async def get(self, user_id: int) -> T | None:
        ...

    @abstractmethod
    async def save(self, user_id: int, schema: T) -> None:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        ...
