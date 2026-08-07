from src.ai.base.agent import BaseAgent
from src.pipelines.reels.config import PROMPTS_PATH
from src.pipelines.reels.schemas.idea import GenerateIdeaInput, GenerateIdeasOutput


class GenerateIdeasAgent(BaseAgent[GenerateIdeaInput, GenerateIdeasOutput]):
    PROMPT_PATH: str = PROMPTS_PATH / "idea" / "generate_ideas.md"
    OUTPUT_SCHEME: type[GenerateIdeasOutput] = GenerateIdeasOutput
