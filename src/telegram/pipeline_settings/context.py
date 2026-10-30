from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class SettingsAction(StrEnum):
    START = "start"

    SELECT_PIPELINE = "select_pipeline"
    SELECT_STEP = "select_step"
    SELECT_ALL_STEPS = "select_all_steps"

    SELECT_SETTINGS = "select_setting"

    SELECT_PROVIDER = "select_provider"
    SELECT_MODEL = "select_models"
    SAVE_MODEL = "save_model"

    SELECT_TEMPERATURE = "select_temperature"
    SAVE_TEMPERATURE = "save_temperature"


class SettingsScope(StrEnum):
    PIPELINE = "pipeline"
    STEP = "step"


class SettingsContext(BaseModel):
    action: SettingsAction = SettingsAction.START
    scope: SettingsScope = SettingsScope.STEP

    user_id: UUID
    pipeline_id: UUID | None = None
    step_id: UUID | None = None
    provider_id: UUID | None = None
    model_id: UUID | None = None
