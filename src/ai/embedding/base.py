from abc import ABC, abstractmethod

from src.core.logging.mixin import LoggedMixin


class BaseEmbedding(ABC, LoggedMixin):
    __log_layer__ = "embedding"

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        ...