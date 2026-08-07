from pydantic import BaseModel

from src.ai.models.enum import Model
from src.pipelines.reels.enums import Agent


class PipelineConfig(BaseModel):
    model: Model
    agent: Agent
    temperature: float = 0.0
    max_tokens: int | None = None
    top_p: float | None = None
    frequency_penalty: float | None = None
    presence_penalty: float | None = None
