from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field

from src.core.enums import Language


class ReelsAction(StrEnum):
    START = "start"

    SELECT_PIPELINE = "select_pipeline"
    SELECT_NICHE = "select_niche"
    SELECT_LANGUAGE = "select_language"
    SELECT_IDEA = "select_idea"
    MORE_IDEAS = "more_ideas"
    EDIT_STORY = "edit_story"


class ReelsContext(BaseModel):
    action: ReelsAction = ReelsAction.START

    user_id: UUID
    pipeline_id: UUID | None = None
    niche_id: UUID | None = None
    session_id: UUID | None = None
    idea_message_ids: list[int] = Field(default_factory=list)
    language: Language | str | None = None
