from langchain_core.language_models import BaseChatModel
from langchain_openrouter import ChatOpenRouter

from src.ai.providers.base import BaseProvider
from src.application.pipeline.schemas import PipelineStepWithUserSettingsSchema


class OpenRouterProvider(BaseProvider):
    provider = "openrouter"

    def create_chat_model(self, pipeline_step: PipelineStepWithUserSettingsSchema) -> BaseChatModel:
        return ChatOpenRouter(
            api_key=self._settings.openrouter_api_key,
            base_url=self._settings.openrouter_base_url,
            model=pipeline_step.user_settings.model.name,
            temperature=pipeline_step.user_settings.temperature,
        )
