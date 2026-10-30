from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field

from src.core.enums import Language
from src.pipelines.reels.idea.schemas import GenerateIdeaOutput
from src.pipelines.reels.story.schemas import GenerateStoryOutput
from src.pipelines.reels.critic.schemas import CritiqueStoryOutput


class IdeaAction(StrEnum):
    CHOOSE = "choose"
    REGENERATE = "regenerate"


class StoryAction(StrEnum):
    APPROVE = "approve"
    EDIT = "edit"


class ReelsState(BaseModel):
    """Serializable state for one Reels workflow run.

    LangGraph persists this state in its checkpointer. The SQLAlchemy
    UserPipelineSession row stores application-facing status and ownership.
    """

    user_id: UUID
    niche: str
    language: Language = Language.UA
    ideas_count: int = 10

    ideas: list[GenerateIdeaOutput] = Field(default_factory=list)
    generated_ideas: list[GenerateIdeaOutput] = Field(default_factory=list)
    selected_idea: GenerateIdeaOutput | None = None
    idea_action: IdeaAction | None = None
    idea_instructions: list[str] = Field(default_factory=list)
    idea_regenerations: int = 0

    story: GenerateStoryOutput | None = None
    critique: CritiqueStoryOutput | None = None
    story_action: StoryAction | None = None
    story_instructions: list[str] = Field(default_factory=list)
    story_edits: int = 0
    is_approved: bool = False
