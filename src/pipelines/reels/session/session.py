from src.core.logging.mixin import LoggedMixin
from src.database.redis.repositories.base import BaseRepository
from src.pipelines.reels.session.config import ReelsSessionConfig


class ReelsPipelineSession:

    def __init__(self, repository: BaseRepository) -> None:
        self._repository = repository

    async def get_session(self, user_id: int, niche: str | None = None) -> ReelsSessionConfig:
        session = await self._repository.get(user_id=user_id)
        return session if session else ReelsSessionConfig(niche=niche)


    async def save_session(self, user_id: int, session: ReelsSessionConfig) -> None:
        await self._repository.save(user_id=user_id, schema=session)


    async def delete_session(self, user_id: int) -> None:
        await self._repository.delete(user_id=user_id)
