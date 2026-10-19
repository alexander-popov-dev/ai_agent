from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field

from src.pipelines.reels.critic.schemas import CritiqueStoryOutput
from src.pipelines.reels.idea.schemas import GenerateIdeaOutput
from src.pipelines.reels.story.schemas import GenerateStoryOutput
from src.pipelines.reels.workflow.state import ReelsState


class ChooseIdeaPrompt(BaseModel):
    type: Literal["choose_idea"]
    message: str
    ideas: list[GenerateIdeaOutput]
    can_regenerate: bool


class ReviewStoryPrompt(BaseModel):
    type: Literal["review_story"]
    message: str
    story: GenerateStoryOutput
    critique: CritiqueStoryOutput | None = None
    can_edit: bool


WorkflowInterrupt = Annotated[
    ChooseIdeaPrompt | ReviewStoryPrompt,
    Field(discriminator="type"),
]


class ReelsWorkflowResponse(BaseModel):
    """Typed result returned to the Telegram/API adapter."""

    session_id: UUID
    state: ReelsState
    interrupt: WorkflowInterrupt | None = None

    @property
    def is_waiting_for_user(self) -> bool:
        return self.interrupt is not None
