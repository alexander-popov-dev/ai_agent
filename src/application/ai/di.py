from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ai.repository import AIProviderRepository, AIModelRepository
from src.application.ai.services import AIService
from src.core.logging.mixin import LoggedMixin


class AIProviderProvider(Provider, LoggedMixin):

    @provide(scope=Scope.REQUEST)
    def get_provider_repository(self, session: AsyncSession) -> AIProviderRepository:
        return AIProviderRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_model_repository(self, session: AsyncSession) -> AIModelRepository:
        return AIModelRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_service(
            self,
            provider_repo: AIProviderRepository,
            model_repo: AIModelRepository
    ) -> AIService:
        return AIService(
            provider_repo=provider_repo,
            model_repo=model_repo
        )
