from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker, create_async_engine,
)

from src.database.postgres.settings import get_database_settings

settings = get_database_settings()


class DatabaseEngine:
    def __init__(self) -> None:
        self.engine = create_async_engine(url=settings.url, echo=True)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        await self.engine.dispose()
