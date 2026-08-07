from src.pipelines.reels.agents.ideas import GenerateIdeasAgent
from src.pipelines.reels.agents.story import GenerateStoryAgent, EditStoryAgent, ParseUserAnswerAgent
from src.pipelines.reels.enums import Agent

AGENTS = {
    Agent.GENERATE_IDEAS: GenerateIdeasAgent,
    Agent.GENERATE_STORY: GenerateStoryAgent,
    Agent.EDIT_STORY: EditStoryAgent,
    Agent.PARSE_STORY_EDIT: ParseUserAnswerAgent,
}