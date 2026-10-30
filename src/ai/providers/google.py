from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI

from src.ai.providers.base import BaseProvider
from src.application.pipeline.schemas import PipelineStepWithUserSettingsSchema


class GoogleProvider(BaseProvider):
    provider = "google"

    def create_chat_model(self, pipeline_step: PipelineStepWithUserSettingsSchema) -> BaseChatModel:
        return ChatGoogleGenerativeAI(
            google_api_key=self._settings.google_api_key,
            model=pipeline_step.user_settings.model.name,
            temperature=pipeline_step.user_settings.temperature,
        )
