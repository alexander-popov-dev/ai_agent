from qdrant_client import AsyncQdrantClient

from src.database.qdrant.settings import get_settings, QdrantSettings


class QdrantFactory:

    def __init__(self):
        self._settings: QdrantSettings = get_settings()

    async def create(self) -> AsyncQdrantClient:
        return AsyncQdrantClient(
        host=self._settings.qdrant_host,
        port=self._settings.qdrant_port,
    )
