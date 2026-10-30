from dishka import Provider, provide, Scope
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from src.application.pipeline.repository import UserPipelineSessionRepository
from src.application.pipeline.service import PipelineService
from src.pipelines.reels.workflow.service import ReelsPipelineService

from src.core.logging.mixin import LoggedMixin


class ReelsPipelineProvider(Provider, LoggedMixin):

    @provide(scope=Scope.REQUEST)
    def get_reels_pipeline_service(
            self,
            checkpointer: AsyncPostgresSaver,
            pipeline_service: PipelineService,
            session: UserPipelineSessionRepository,
    ) -> ReelsPipelineService:
        return ReelsPipelineService(
            checkpointer=checkpointer,
            pipeline_service=pipeline_service,
            session=session
        )
