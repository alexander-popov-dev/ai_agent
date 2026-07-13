from abc import ABC, abstractmethod


class BaseEmbedding(ABC):

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        ...