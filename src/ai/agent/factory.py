from src.ai.agent.base import BaseAgent
from src.ai.prompt.factory import PromptFactory
from src.ai.providers.factory import ProviderFactory
from src.application.pipeline.schemas import PipelineStepWithUserSettingsSchema


class AgentFactory:

    @staticmethod
    def create(pipeline_step: PipelineStepWithUserSettingsSchema) -> BaseAgent:
        agent_cls = BaseAgent.get_agent(agent=pipeline_step.agent)

        return agent_cls(
            model=ProviderFactory.create(pipeline_step=pipeline_step),
            prompt=PromptFactory.create(pipeline_step=pipeline_step),
        )
