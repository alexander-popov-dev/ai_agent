from langchain_core.prompts import ChatPromptTemplate

from src.application.pipeline.schemas import PipelineStepWithUserSettingsSchema
from src.core.logging.mixin import LoggedMixin


class PromptFactory(LoggedMixin):

    @classmethod
    def create(cls, pipeline_step: PipelineStepWithUserSettingsSchema) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            messages=[
                ("system", pipeline_step.system_prompt),
                ("human", pipeline_step.user_prompt or "Process the input.")
            ]
        )
