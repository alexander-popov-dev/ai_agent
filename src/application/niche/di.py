from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.niche.repository import NicheRepository
from src.application.niche.service import NicheService
from src.core.logging.mixin import LoggedMixin


class NicheProvider(Provider, LoggedMixin):

    @provide(scope=Scope.REQUEST)
    def get_repository(self, session: AsyncSession) -> NicheRepository:
        return NicheRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_service(self, repository: NicheRepository) -> NicheService:
        return NicheService(repository=repository)
