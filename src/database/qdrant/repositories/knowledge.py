from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct

from src.ai.embedding.base import BaseEmbedding
from src.ai.knowledge.schema import KnowledgeDocument
from src.database.qdrant.repositories.base import BaseRepository


class Knowledge(BaseRepository):

    def __init__(
            self,
            embedding: BaseEmbedding,
            client: AsyncQdrantClient,
            collection_name: str
    ) -> None:
        self._embedding = embedding
        self._client = client
        self._collection_name = collection_name

    async def add(self, document: KnowledgeDocument) -> None:
        vector = await self._embedding.embed(text=document.content)
        await  self._client.upsert(
            collection_name=self._collection_name,
            points=[
                PointStruct(
                    id=document.id,
                    vector=vector,
                    payload=document.model_dump(mode="json")
                )
            ]
        )

    async def search(self, query: str, limit: int = 5) -> list[KnowledgeDocument]:
        vector = await self._embedding.embed(text=query)
        result = await self._client.query_points(
            collection_name=self._collection_name,
            query=vector,
            limit=limit,
            # score_threshold=0.7
        )
        return [
            KnowledgeDocument.model_validate(point.payload)
            for point in result.points
        ]
