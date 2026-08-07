from langchain_core.language_models import BaseChatModel

from src.ai.base.agent import BaseAgent
from src.pipelines.core.prompt_loader import PromptLoader
from src.pipelines.reels.agents.registry import AGENTS
from src.pipelines.reels.enums import Agent


class AgentFactory:

    @staticmethod
    def create(agent: Agent, llm: BaseChatModel) -> BaseAgent:
        agent_cls = AGENTS.get(agent)

        if agent_cls is None:
            raise ValueError(f"Agent {agent} is not supported")

        prompt = PromptLoader.load(path=agent_cls.PROMPT_PATH)

        return agent_cls(llm=llm, prompt=prompt)
