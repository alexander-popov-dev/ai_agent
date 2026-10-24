from abc import ABC, abstractmethod

from langchain_core.language_models import BaseChatModel

from src.application.pipeline.schemas import PipelineStepWithUserSettingsSchema
from src.core.logging.mixin import LoggedMixin


class BaseProvider(ABC, LoggedMixin):

    @abstractmethod
    def create_chat_model(self, pipeline_step: PipelineStepWithUserSettingsSchema) -> BaseChatModel:
        ...
