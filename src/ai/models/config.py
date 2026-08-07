from pydantic import BaseModel

from src.ai.models.enum import Model
from src.ai.providers.enum import Provider
from src.paths import BASE_DIR

MODELS_PATH = BASE_DIR / "src" / "ai" / "models" / "models.yaml"

class ModelConfig(BaseModel):
    provider: Provider
    model: str


class ModelsConfig(BaseModel):
    models: dict[Model, ModelConfig]