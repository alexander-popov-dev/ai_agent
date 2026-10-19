from src.application.ai.repository import AIProviderRepository
from src.application.ai.schemas import AIProviderSchema


class AIProviderService:
    def __init__(self, repository: AIProviderRepository) -> None:
        self._repository = repository

    async def get_providers_with_models(self) -> list[AIProviderSchema]:
        result = await self._repository.get_providers_with_models()
        return [AIProviderSchema.model_validate(provider) for provider in result]