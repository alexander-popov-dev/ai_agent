from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.application.ai.schemas import AIModelSchema
from src.pipelines.core.enums import PipelineSessionStatus


class UserStepSettingsSchema(BaseModel):
    id: UUID
    user_id: UUID
    step_id: UUID
    model_id: UUID
    temperature: float | int


class UserStepSettingsWithModelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    step_id: UUID
    model: AIModelSchema
    temperature: float | int


class UserStepSettingsUpdateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: UUID
    step_id: UUID
    model_id: UUID | None = None
    temperature: float | int | None = None


class PipelineStepSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    display_name: str
    agent: str
    order: int
    system_prompt: str
    user_prompt: str | None

    user_settings: UserStepSettingsWithModelSchema | None = None


class PipelineSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    display_name: str


class UserPipelineSessionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    pipeline_id: UUID
    step_id: UUID | None = None
    status: PipelineSessionStatus = PipelineSessionStatus.CREATED
    error_message: str | None = None
    error_traceback: str | None = None
