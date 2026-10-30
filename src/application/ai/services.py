from uuid import UUID

from src.application.ai.repository import AIProviderRepository, AIModelRepository
from src.application.ai.schemas import AIProviderSchema, AIModelSchema


class AIService:
    def __init__(
            self,
            provider_repo: AIProviderRepository,
            model_repo: AIModelRepository
    ) -> None:
        self._provider_repo = provider_repo
        self._model_repo = model_repo

    async def get_providers(self) -> list[AIProviderSchema]:
        result = await self._provider_repo.get_providers()
        return [AIProviderSchema.model_validate(provider) for provider in result]

    async def get_models(self, provider_id: UUID) -> list[AIModelSchema]:
        result = await self._model_repo.get_models(provider_id=provider_id)
        return [AIModelSchema.model_validate(provider) for provider in result]

    async def get_providers_with_models(self) -> list[AIProviderSchema]:
        result = await self._provider_repo.get_providers_with_models()
        return [AIProviderSchema.model_validate(provider) for provider in result]
