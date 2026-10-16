from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama

from ai import ModelConfig, ProviderConfig
from ai.providers.base import BaseProvider
from src.pipelines.core.config import PipelineConfig


class OllamaProvider(BaseProvider):

    def create_chat_model(
            self,
            provider_config: ProviderConfig,
            model_config: ModelConfig,
            pipeline_config: PipelineConfig,
    ) -> BaseChatModel:

        return ChatOllama(
            base_url=provider_config.base_url,
            model=model_config.model,
            temperature=pipeline_config.temperature,
        )
