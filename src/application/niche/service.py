from uuid import UUID

from src.application.niche.repository import NicheRepository
from src.application.niche.schemas import NicheScheme


class NicheService:
    def __init__(self, repository: NicheRepository) -> None:
        self._repository = repository

    async def get_niche(self, niche_id: UUID) -> NicheScheme:
        result = await self._repository.get_by_id(id_=niche_id)
        return NicheScheme.model_validate(result)

    async def get_all_by_user(self, user_id: UUID | str) -> list[NicheScheme] | None:
        result = await self._repository.get_all_by_user(user_id=user_id)
        return [NicheScheme.model_validate(niche) for niche in result]
