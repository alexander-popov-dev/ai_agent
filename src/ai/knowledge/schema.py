from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class KnowledgeDocument(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    category: str
    source: str
    title: str
    content: str
    tags: list[str]