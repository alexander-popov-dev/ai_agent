from typing import Any

from langgraph.types import interrupt
from pydantic import BaseModel

from src.ai.agent.factory import AgentFactory
from src.application.pipeline.schemas import PipelineStepWithUserSettingsSchema
from src.pipelines.reels.critic.schemas import CritiqueStoryInput
from src.pipelines.reels.enums import ReelsAgent
from src.pipelines.reels.idea.schemas import GenerateIdeaInput, IdeaContext
from src.pipelines.reels.story.schemas import GenerateStoryInput, StoryContext, EditStoryInput
from src.pipelines.reels.workflow.decisions import ChooseIdeaDecision, ReviewStoryDecision, ChooseIdeaAction
from src.pipelines.reels.workflow.state import IdeaAction, ReelsState, StoryAction

MAX_IDEA_REGENERATIONS = 5
MAX_STORY_EDITS = 5


def _json_model(value: BaseModel) -> dict[str, Any]:
    """Convert a Pydantic value into JSON-compatible data for an interrupt payload."""
    return value.model_dump(mode="json")


class ReelsWorkflowNodes:
    """Node implementations. AI work is delegated to the existing ReelsPipeline."""

    def __init__(self, pipeline_steps: list[PipelineStepWithUserSettingsSchema]) -> None:
        self.__steps = {step.agent: step for step in pipeline_steps}
        self._generate_ideas = AgentFactory.create(pipeline_step=self.__steps[ReelsAgent.GENERATE_IDEAS])
        self._generate_story = AgentFactory.create(pipeline_step=self.__steps[ReelsAgent.GENERATE_STORY])
        self._edit_story = AgentFactory.create(pipeline_step=self.__steps[ReelsAgent.EDIT_STORY])
        self._critique_story = AgentFactory.create(pipeline_step=self.__steps[ReelsAgent.CRITIQUE_STORY])

    async def generate_ideas(self, state: ReelsState) -> ReelsState:
        result = await self._generate_ideas.execute(
            payload=GenerateIdeaInput(
                niche=state.niche,
                language=state.language,
                ideas_count=state.ideas_count,
                ideas=state.generated_ideas,
                instructions=IdeaContext(instructions=state.idea_instructions),
            )
        )
        if not result.ideas:
            raise ValueError("The ideas agent returned no ideas")

        # Keep existing ideas so the user can choose from the entire list.
        state.generated_ideas = [*state.generated_ideas, *result.ideas]
        state.ideas = result.ideas
        state.idea_instructions = []
        state.idea_action = None

        return state

    def choose_idea(self, state: ReelsState) -> ReelsState:
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

            state.idea_action = IdeaAction.REGENERATE
            state.idea_instructions = [*state.idea_instructions, (decision.instruction or "").strip()]
            state.idea_regenerations = state.idea_regenerations + 1

            return state

        assert decision.idea_index is not None

        if decision.idea_index >= len(state.ideas):
            raise ValueError("Selected idea index is outside the available ideas")

        state.selected_idea = state.ideas[decision.idea_index]
        state.idea_action = IdeaAction.CHOOSE

        return state

    async def generate_story(self, state: ReelsState) -> ReelsState:
        if state.selected_idea is None:
            raise ValueError("Cannot generate a story before an idea is selected")

        story = await self._generate_story.execute(
            payload=GenerateStoryInput(
                idea=state.selected_idea,
                language=state.language,
                instructions=StoryContext(instructions=state.story_instructions),
            )
        )

        state.story = story
        state.critique = None
        state.story_action = None
        state.is_approved = False

        return state

    async def critique_story(self, state: ReelsState) -> ReelsState:
        if state.story is None:
            raise ValueError("Cannot critique a story before it has been generated")

        critique = await self._critique_story.execute(
            payload=CritiqueStoryInput(
                caption=state.story.caption,
                narration=state.story.narration,
                language=state.language,
            )
        )

        state.critique = critique

        return state

    def review_story(self, state: ReelsState) -> ReelsState:
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
            state.story_action = StoryAction.APPROVE
            state.is_approved = True
            return state

        if state.story_edits >= MAX_STORY_EDITS:
            raise ValueError("The maximum number of story edits has been reached")

        state.story_action = StoryAction.EDIT
        state.story_instructions = [*state.story_instructions, decision.instruction.strip()]
        state.story_edits = state.story_edits + 1
        state.is_approved = False

        return state

    async def edit_story(self, state: ReelsState) -> ReelsState:
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

        state.story = edited_story
        state.critique = None
        state.story_action = None

        return state
