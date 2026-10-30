from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama

from src.ai.providers.base import BaseProvider
from src.application.pipeline.schemas import PipelineStepWithUserSettingsSchema


class OllamaProvider(BaseProvider):
    provider = "ollama"

    def create_chat_model(self, pipeline_step: PipelineStepWithUserSettingsSchema) -> BaseChatModel:
        return ChatOllama(
            base_url=self._settings.ollama_base_url,
            model=pipeline_step.user_settings.model.name,
            temperature=pipeline_step.user_settings.temperature,
        )
