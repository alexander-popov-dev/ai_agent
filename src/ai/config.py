from pydantic import BaseModel

from src.ai.models.config import ModelConfig
from src.ai.models.enum import Model
from src.ai.providers.config import ProviderConfig
from src.ai.providers.enum import Provider


class AIConfig(BaseModel):
    providers: dict[Provider, ProviderConfig]
    models: dict[Model, ModelConfig]
