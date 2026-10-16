from langchain_core.language_models import BaseChatModel

from ai.agent.base import BaseAgent
from src.pipelines.core.prompt_loader import PromptLoader
from src.pipelines.reels.agents.registry import AGENTS
from src.pipelines.reels.enums import Agent


class AgentFactory:

    @staticmethod
    def create(agent: Agent, model: BaseChatModel) -> BaseAgent:
        agent_cls = AGENTS.get(agent)

        if agent_cls is None:
            raise ValueError(f"Agent {agent} is not supported")

        prompt = PromptLoader.load(path=agent_cls.prompt_path)

        return agent_cls(model=model, prompt=prompt)
