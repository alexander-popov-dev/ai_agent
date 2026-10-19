from src.database.redis.repositories.base import BaseRepository
from src.telegram.reels.session.config import ReelsSessionConfig


class ReelsPipelineSession:

    def __init__(self, repository: BaseRepository) -> None:
        self._repository = repository

    async def get_session(self, user_id: int, niche: str | None) -> ReelsSessionConfig:
        session = await self._repository.get(user_id=user_id)

        if isinstance(session, ReelsSessionConfig):
            return session

        if niche:
            return ReelsSessionConfig(niche=niche)

        raise ValueError("Niche not provided")


    async def save_session(self, user_id: int, session: ReelsSessionConfig) -> None:
        await self._repository.save(user_id=user_id, schema=session)


    async def delete_session(self, user_id: int) -> None:
        await self._repository.delete(user_id=user_id)
