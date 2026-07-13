from abc import ABC, abstractmethod

from src.application.session import Session


class BaseRepository(ABC):
    @abstractmethod
    async def get(self, user_id: int) -> Session:
        ...

    @abstractmethod
    async def save(self, user_id: int, schema: Session) -> None:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        ...
