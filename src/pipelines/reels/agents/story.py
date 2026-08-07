from src.ai.base.agent import BaseAgent
from src.pipelines.reels.config import PROMPTS_PATH
from src.pipelines.reels.schemas.story import GenerateStoryInput, GenerateStoryOutput, ParseUserAnswerInput, \
    ParseUserAnswerOutput, EditStoryInput, EditStoryOutput


class GenerateStoryAgent(BaseAgent[GenerateStoryInput, GenerateStoryOutput]):
    PROMPT_PATH: str = PROMPTS_PATH / "story" / "generate_story.md"
    OUTPUT_SCHEME = GenerateStoryOutput


class ParseUserAnswerAgent(BaseAgent[ParseUserAnswerInput, ParseUserAnswerOutput]):
    PROMPT_PATH: str = PROMPTS_PATH / "parser" / "user_answer.md"
    OUTPUT_SCHEME = ParseUserAnswerOutput


class EditStoryAgent(BaseAgent[EditStoryInput, EditStoryOutput]):
    PROMPT_PATH: str = PROMPTS_PATH / "story" / "edit_story.md"
    OUTPUT_SCHEME = EditStoryOutput
