from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct

from src.ai.embedding.base import BaseEmbedding
from src.ai.knowledge.schema import KnowledgeDocument
from src.database.qdrant.repositories.base import BaseRepository


class Knowledge(BaseRepository):

    COLLECTION = "reels_patent_knowledge"

    def __init__(
            self,
            embedding: BaseEmbedding,
            client: AsyncQdrantClient
    ) -> None:
        self._embedding = embedding
        self._client = client

    async def add(self, document: KnowledgeDocument) -> None:
        vector = await self._embedding.embed(text=document.content)
        await  self._client.upsert(
            collection_name=self.COLLECTION,
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
            collection_name=self.COLLECTION,
            query=vector,
            limit=limit
        )
        return [
            KnowledgeDocument.model_validate(point.payload)
            for point in result.points
        ]
