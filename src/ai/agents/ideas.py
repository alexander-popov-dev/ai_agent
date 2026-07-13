from src.ai.agents.base import BaseAgent
from src.ai.schemas.idea import (
    GenerateIdeasOutput,
    GenerateIdeaInput,
    ImproveIdeaInput,
    ImproveIdeaOutput
)


class GenerateIdeasAgent(
    BaseAgent[
        GenerateIdeaInput,
        GenerateIdeasOutput
    ]
):
    PROMPT_NAME: str = "idea"
    OUTPUT_SCHEME: type[GenerateIdeasOutput] = GenerateIdeasOutput


class ImproveIdeaAgent(
    BaseAgent[
        ImproveIdeaInput,
        ImproveIdeaOutput
    ]
):
    PROMPT_NAME: str = "improve_idea"
    OUTPUT_SCHEME: type[GenerateIdeasOutput] = GenerateIdeasOutput
