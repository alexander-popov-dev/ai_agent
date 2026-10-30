from langchain_core.language_models import BaseChatModel
from langchain_groq import ChatGroq
from src.ai.providers.base import BaseProvider
from src.application.pipeline.schemas import PipelineStepWithUserSettingsSchema


class GroqProvider(BaseProvider):
    provider = "groq"

    def create_chat_model(self, pipeline_step: PipelineStepWithUserSettingsSchema) -> BaseChatModel:
        return ChatGroq(
            api_key=self._settings.groq_api_key,
            model=pipeline_step.user_settings.model.name,
            temperature=pipeline_step.user_settings.temperature,
        )
