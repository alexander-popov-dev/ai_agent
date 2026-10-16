from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, START, StateGraph

from src.pipelines.reels.pipeline import ReelsPipeline
from src.pipelines.reels.workflow.nodes import ReelsWorkflowNodes
from src.pipelines.reels.workflow.state import IdeaAction, ReelsState, StoryAction


def _after_idea_choice(raw_state: ReelsState | dict) -> str:
    state = raw_state if isinstance(raw_state, ReelsState) else ReelsState.model_validate(raw_state)
    if state.idea_action == IdeaAction.CHOOSE:
        return "generate_story"
    return "generate_ideas"


def _after_story_review(raw_state: ReelsState | dict) -> str:
    state = raw_state if isinstance(raw_state, ReelsState) else ReelsState.model_validate(raw_state)
    if state.story_action == StoryAction.APPROVE or state.is_approved:
        return "finish"
    return "edit_story"


def build_reels_graph(
    pipeline: ReelsPipeline,
    checkpointer: BaseCheckpointSaver,
):
    """Build the Reels graph once and reuse it for all sessions.

    A separate thread_id (the UserPipelineSession UUID) isolates each run.
    """
    nodes = ReelsWorkflowNodes(pipeline)
    builder = StateGraph(ReelsState)

    builder.add_node("generate_ideas", nodes.generate_ideas)
    builder.add_node("choose_idea", nodes.choose_idea)
    builder.add_node("generate_story", nodes.generate_story)
    builder.add_node("critique_story", nodes.critique_story)
    builder.add_node("review_story", nodes.review_story)
    builder.add_node("edit_story", nodes.edit_story)

    builder.add_edge(START, "generate_ideas")
    builder.add_edge("generate_ideas", "choose_idea")
    builder.add_conditional_edges(
        "choose_idea",
        _after_idea_choice,
        {"generate_ideas": "generate_ideas", "generate_story": "generate_story"},
    )
    builder.add_edge("generate_story", "critique_story")
    builder.add_edge("critique_story", "review_story")
    builder.add_conditional_edges(
        "review_story",
        _after_story_review,
        {"edit_story": "edit_story", "finish": END},
    )
    builder.add_edge("edit_story", "critique_story")

    return builder.compile(checkpointer=checkpointer)
