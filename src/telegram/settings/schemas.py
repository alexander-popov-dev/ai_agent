from pydantic import BaseModel, Field

from src.application.ai.schemas import AIProviderSchema
from src.application.pipeline.schemas import PipelineSchema, PipelineStepSchema
from src.application.user.schemas import UserSchema


class SettingsSessionSchema(BaseModel):
    user: UserSchema
    pipeline: PipelineSchema | None = None
    step_id: str | None = None
    model_id: str | None = None
    steps: list[PipelineStepSchema] = Field(default_factory=list)
    providers: list[AIProviderSchema] = Field(default_factory=list)
