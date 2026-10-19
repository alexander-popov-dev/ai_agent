from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ai.repository import AIProviderRepository
from src.application.ai.services import AIProviderService
from src.core.logging.mixin import LoggedMixin


class AIProviderProvider(Provider, LoggedMixin):

    @provide(scope=Scope.REQUEST)
    def get_repository(self, session: AsyncSession) -> AIProviderRepository:
        return AIProviderRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_service(self, repository: AIProviderRepository) -> AIProviderService:
        return AIProviderService(repository=repository)
