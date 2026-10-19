from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI

from ai import ModelConfig, ProviderConfig
from ai.providers.base import BaseProvider
from src.pipelines.core.config import PipelineConfig


class GoogleProvider(BaseProvider):

    def create_chat_model(
            self,
            provider_config: ProviderConfig,
            model_config: ModelConfig,
            pipeline_config: PipelineConfig,
    ) -> BaseChatModel:

        return ChatGoogleGenerativeAI(
            google_api_key=provider_config.api_key,
            model=model_config.model,
            temperature=pipeline_config.temperature,
        )
