from abc import ABC, abstractmethod

from langchain_core.language_models import BaseChatModel

from src.core.logging.mixin import LoggedMixin
from src.pipelines.core.config import PipelineConfig


class BaseProvider(ABC, LoggedMixin):
    __log_layer__ = "provider"

    @abstractmethod
    def create_chat_model(
            self,
            provider_config: ProviderConfig,
            model_config: ModelConfig,
            pipeline_config: PipelineConfig
    ) -> BaseChatModel:
        ...
