from langchain_ollama import OllamaEmbeddings

from src.ai.embedding.base import BaseEmbedding


class OllamaEmbedding(BaseEmbedding):

    def __init__(self, model: str, base_url: str) -> None:
        self._model = model
        self._base_url = base_url
        self._embedding = OllamaEmbeddings(model=model, base_url=base_url)

    async def embed(self, text: str) -> list[float]:
        return await self._embedding.aembed_query(text=text)
