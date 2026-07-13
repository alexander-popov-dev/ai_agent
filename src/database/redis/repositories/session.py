from os import name

from redis.asyncio import Redis

from src.application.session import Session
from src.database.redis.repositories.base import BaseRepository


class RedisSessionRepository(BaseRepository):
    PREFIX = "session"

    def __init__(self, client: Redis):
        self._client = client

    async def get(self, user_id: int) -> Session | None:
        session = await self._client.get(name=f"{self.PREFIX}:{user_id}")
        if session:
            return Session.model_validate_json(json_data=session)
        return None

    async def save(self, user_id: int, schema: Session) -> None:
        await self._client.set(name=f"{self.PREFIX}:{user_id}", value=schema.model_dump_json())

    async def delete(self, user_id: int) -> None:
        await self._client.delete(f"{self.PREFIX}:{user_id}")