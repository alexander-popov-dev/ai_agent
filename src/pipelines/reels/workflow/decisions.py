from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class ChooseIdeaAction(StrEnum):
    choose = "choose"
    regenerate = "regenerate"


class ReviewStoryAction(StrEnum):
    approve = "approve"
    edit = "edit"


class ChooseIdeaDecision(BaseModel):
    """Validated Telegram response to the idea-selection interrupt.

    idea_index is zero-based and refers to the complete list displayed to the user.
    """

    action: ChooseIdeaAction
    idea_index: int | None = Field(default=None, ge=0)
    instruction: str | None = None

    @model_validator(mode="after")
    def validate_decision(self) -> "ChooseIdeaDecision":
        if self.action == self.action.choose and self.idea_index is None:
            raise ValueError("idea_index is required when action='choose'")
        if self.action == self.action.regenerate and not (self.instruction or "").strip():
            raise ValueError("instruction is required when action='regenerate'")
        if self.action == self.action.choose and self.instruction:
            raise ValueError("instruction is not accepted when choosing an idea")
        return self


class ReviewStoryDecision(BaseModel):
    """Validated Telegram response to the story-review interrupt."""

    action: ReviewStoryAction
    instruction: str | None = None

    @model_validator(mode="after")
    def validate_decision(self) -> "ReviewStoryDecision":
        if self.action == self.action.edit and not (self.instruction or "").strip():
            raise ValueError("instruction is required when action='edit'")
        return self
