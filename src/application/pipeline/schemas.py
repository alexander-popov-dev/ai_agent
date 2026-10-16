from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.pipelines.core.enums import PipelineSessionStatus


class UserStepSettingsSchema(BaseModel):
    id: UUID
    model: str
    temperature: float | int


class PipelineStepSchema(BaseModel):
    id: UUID
    name: str
    display_name: str
    agent: str
    order: int
    system_prompt: str
    user_prompt: str | None

    user_settings: UserStepSettingsSchema | None = None

    model_config = ConfigDict(from_attributes=True)


class PipelineSchema(BaseModel):
    id: UUID
    name: str
    display_name: str

    model_config = ConfigDict(from_attributes=True)


class UserPipelineSessionSchema(BaseModel):
    user_id: UUID
    pipeline_id: UUID
    step_id: UUID | None = None
    status: PipelineSessionStatus =PipelineSessionStatus.CREATED
    error_message: str | None = None
    error_traceback: str | None = None

    model_config = ConfigDict(from_attributes=True)
