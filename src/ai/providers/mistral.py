from langchain_core.language_models import BaseChatModel
from langchain_mistralai import ChatMistralAI

from src.ai.providers.base import BaseProvider
from src.application.pipeline.schemas import PipelineStepWithUserSettingsSchema


class MistralProvider(BaseProvider):
    provider = "mistral"

    def create_chat_model(self, pipeline_step: PipelineStepWithUserSettingsSchema) -> BaseChatModel:
        return ChatMistralAI(
            mistral_api_key=self._settings.mistral_api_key,
            model=pipeline_step.user_settings.model.name,
            temperature=pipeline_step.user_settings.temperature,
        )
