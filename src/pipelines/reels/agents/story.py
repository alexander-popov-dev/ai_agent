from src.ai.base.agent import BaseAgent
from src.pipelines.reels.config import PROMPTS_PATH
from src.pipelines.reels.schemas.story import GenerateStoryInput, GenerateStoryOutput, EditStoryInput


class GenerateStoryAgent(BaseAgent[GenerateStoryInput, GenerateStoryOutput]):
    PROMPT_PATH: str = PROMPTS_PATH / "story" / "generate_story.md"
    OUTPUT_SCHEME = GenerateStoryOutput


class EditStoryAgent(BaseAgent[EditStoryInput, GenerateStoryOutput]):
    PROMPT_PATH: str = PROMPTS_PATH / "story" / "edit_story.md"
    OUTPUT_SCHEME = GenerateStoryOutput
