from pydantic import Field

from src.settings import BaseProjectSettings


class QdrantSettings(BaseProjectSettings):
    qdrant_host: str = Field(alias="QDRANT_HOST")
    qdrant_port: int = Field(alias="QDRANT_PORT")


def get_settings() -> QdrantSettings:
    return QdrantSettings()
