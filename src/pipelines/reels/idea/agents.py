from src.ai.agent.base import BaseAgent
from src.pipelines.reels.idea.schemas import GenerateIdeaInput, GenerateIdeasOutput


class GenerateIdeasAgent(BaseAgent[GenerateIdeaInput, GenerateIdeasOutput]):
    agent = "generate_ideas"
    output_schema = GenerateIdeasOutput
