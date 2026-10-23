from typing import Any

from langgraph.types import interrupt
from pydantic import BaseModel

from src.ai.agent.base import BaseAgent
from src.pipelines.reels.critic.schemas import CritiqueStoryInput
from src.pipelines.reels.idea.schemas import GenerateIdeaInput, IdeaContext
from src.pipelines.reels.story.schemas import GenerateStoryInput, StoryContext, EditStoryInput
from src.pipelines.reels.workflow.decisions import ChooseIdeaDecision, ReviewStoryDecision, ChooseIdeaAction
from src.pipelines.reels.workflow.state import IdeaAction, ReelsState, StoryAction

MAX_IDEA_REGENERATIONS = 5
MAX_STORY_EDITS = 5


def _state(value: ReelsState | dict[str, Any]) -> ReelsState:
    """Normalize LangGraph's runtime state to a validated Pydantic object."""
    return value if isinstance(value, ReelsState) else ReelsState.model_validate(value)


def _json_model(value: BaseModel) -> dict[str, Any]:
    """Convert a Pydantic value into JSON-compatible data for an interrupt payload."""
    return value.model_dump(mode="json")


class ReelsWorkflowNodes:
    """Node implementations. AI work is delegated to the existing ReelsPipeline."""

    def __init__(
            self,
            generate_ideas: BaseAgent,
            generate_story: BaseAgent,
            edit_story: BaseAgent,
            critique_story: BaseAgent,
    ) -> None:
        self._generate_ideas = generate_ideas
        self._generate_story = generate_story
        self._edit_story = edit_story
        self._critique_story = critique_story

    async def generate_ideas(self, raw_state: ReelsState | dict[str, Any]) -> dict[str, Any]:
        state = _state(raw_state)
        result = await self._generate_ideas.execute(
            payload=GenerateIdeaInput(
                niche=state.niche,
                language=state.language,
                ideas_count=state.ideas_count,
                ideas=state.ideas,
                instructions=IdeaContext(instructions=state.idea_instructions),
            )
        )
        if not result.ideas:
            raise ValueError("The ideas agent returned no ideas")

        # Keep existing ideas so the user can choose from the entire list.
        return {
            "ideas": [*state.ideas, *result.ideas],
            "idea_instructions": [],
            "idea_action": None,
        }

    def choose_idea(self, raw_state: ReelsState | dict[str, Any]) -> dict[str, Any]:
        state = _state(raw_state)
        decision = ChooseIdeaDecision.model_validate(
            interrupt(
                {
                    "type": "choose_idea",
                    "message": "Choose an idea or ask for more ideas.",
                    "ideas": [_json_model(idea) for idea in state.ideas],
                    "can_regenerate": state.idea_regenerations < MAX_IDEA_REGENERATIONS,
                }
            )
        )

        if decision.action == ChooseIdeaAction.regenerate:
            if state.idea_regenerations >= MAX_IDEA_REGENERATIONS:
                raise ValueError("The maximum number of idea regenerations has been reached")
            return {
                "idea_action": IdeaAction.REGENERATE,
                "idea_instructions": [*state.idea_instructions, decision.instruction.strip()],
                "idea_regenerations": state.idea_regenerations + 1,
            }

        assert decision.idea_index is not None
        if decision.idea_index >= len(state.ideas):
            raise ValueError("Selected idea index is outside the available ideas")

        return {
            "selected_idea": state.ideas[decision.idea_index],
            "idea_action": IdeaAction.CHOOSE,
        }

    async def generate_story(self, raw_state: ReelsState | dict[str, Any]) -> dict[str, Any]:
        state = _state(raw_state)
        if state.selected_idea is None:
            raise ValueError("Cannot generate a story before an idea is selected")

        story = await self._generate_story.execute(
            payload=GenerateStoryInput(
                idea=state.selected_idea,
                language=state.language,
                instructions=StoryContext(instructions=state.story_instructions),
            )
        )
        return {
            "story": story,
            "critique": None,
            "story_action": None,
            "is_approved": False,
        }

    async def critique_story(self, raw_state: ReelsState | dict[str, Any]) -> dict[str, Any]:
        state = _state(raw_state)
        if state.story is None:
            raise ValueError("Cannot critique a story before it has been generated")

        critique = await self._critique_story.execute(
            payload=CritiqueStoryInput(
                caption=state.story.caption,
                narration=state.story.narration,
                language=state.language,
            )
        )
        return {"critique": critique}

    def review_story(self, raw_state: ReelsState | dict[str, Any]) -> dict[str, Any]:
        state = _state(raw_state)
        if state.story is None:
            raise ValueError("Cannot review a story before it has been generated")

        raw_decision = interrupt(
            {
                "type": "review_story",
                "message": "Review the story: approve it or request an edit.",
                "story": _json_model(state.story),
                "critique": _json_model(state.critique) if state.critique else None,
                "can_edit": state.story_edits < MAX_STORY_EDITS,
            }
        )
        decision = ReviewStoryDecision.model_validate(raw_decision)

        if decision.action == "approve":
            return {"story_action": StoryAction.APPROVE, "is_approved": True}

        if state.story_edits >= MAX_STORY_EDITS:
            raise ValueError("The maximum number of story edits has been reached")

        return {
            "story_action": StoryAction.EDIT,
            "story_instructions": [*state.story_instructions, decision.instruction.strip()],
            "story_edits": state.story_edits + 1,
            "is_approved": False,
        }

    async def edit_story(self, raw_state: ReelsState | dict[str, Any]) -> dict[str, Any]:
        state = _state(raw_state)
        if state.story is None:
            raise ValueError("Cannot edit a story before it has been generated")
        if not state.story_instructions:
            raise ValueError("Cannot edit a story without an instruction")

        edited_story = await self._edit_story.execute(
            payload=EditStoryInput(
                story=state.story,
                instruction=state.story_instructions[-1],
                language=state.language,
            )
        )
        return {"story": edited_story, "critique": None, "story_action": None}
