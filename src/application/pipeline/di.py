from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.pipeline.repository import PipelineRepository, PipelineStepRepository, \
    UserPipelineSettingsRepository, UserPipelineSessionRepository
from src.application.pipeline.service import PipelineService
from src.core.logging.mixin import LoggedMixin


class PipelineProvider(Provider, LoggedMixin):

    @provide(scope=Scope.REQUEST)
    async def get_pipeline_repo(self, session: AsyncSession) -> PipelineRepository:
        return PipelineRepository(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_pipeline_step_repo(self, session: AsyncSession) -> PipelineStepRepository:
        return PipelineStepRepository(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_user_pipeline_settings_repo(self, session: AsyncSession) -> UserPipelineSettingsRepository:
        return UserPipelineSettingsRepository(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_user_pipeline_session_repo(self, session: AsyncSession) -> UserPipelineSessionRepository:
        return UserPipelineSessionRepository(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_service(
            self,
            pipeline_repo: PipelineRepository,
            pipeline_step_repo: PipelineStepRepository,
            user_pipeline_settings_repo: UserPipelineSettingsRepository,
            user_pipeline_session_repo: UserPipelineSessionRepository,
    ) -> PipelineService:
        return PipelineService(
            pipeline_repo=pipeline_repo,
            pipeline_step_repo=pipeline_step_repo,
            user_pipeline_settings_repo=user_pipeline_settings_repo,
            user_pipeline_session_repo=user_pipeline_session_repo,
        )
