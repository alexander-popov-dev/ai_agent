from src.ai.agents.base import BaseAgent
from src.ai.schemas.story import StoryInput, StoryOutput


class StoryAgent(BaseAgent[StoryInput, StoryOutput]):
    PROMPT_NAME: str = "story"
    OUTPUT_SCHEME: type[StoryOutput] = StoryOutput
