from abc import ABC, abstractmethod

from src.ai.knowledge.schema import KnowledgeDocument


class BaseRepository(ABC):

    @abstractmethod
    async def add(self, document: KnowledgeDocument) -> None:
        ...

    @abstractmethod
    async def search(self, query: str, limit: int = 5) -> list[KnowledgeDocument]:
        ...
