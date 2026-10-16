from uuid import UUID

from src.application.pipeline.models import UserPipelineSession
from src.application.pipeline.repository import (
    PipelineRepository,
    PipelineStepRepository,
    UserPipelineSettingsRepository, UserPipelineSessionRepository
)
from src.application.pipeline.schemas import PipelineSchema, PipelineStepSchema, UserStepSettingsSchema, \
    UserPipelineSessionSchema


class PipelineService:
    def __init__(
            self,
            pipeline_repo: PipelineRepository,
            pipeline_step_repo: PipelineStepRepository,
            user_pipeline_settings_repo: UserPipelineSettingsRepository,
            user_pipeline_session_repo: UserPipelineSessionRepository
    ) -> None:
        self._pipeline_repo = pipeline_repo
        self._pipeline_step_repo = pipeline_step_repo
        self._user_pipeline_settings_repo = user_pipeline_settings_repo
        self._user_pipeline_session_repo = user_pipeline_session_repo

    async def get_pipelines(self) -> list:
        result = await self._pipeline_repo.get_all()
        return [PipelineSchema.model_validate(pipeline) for pipeline in result]

    async def get_pipline_steps(self, pipeline_id: UUID) -> list[PipelineStepSchema]:
        result = await self._pipeline_step_repo.get_pipline_steps(pipeline_id=pipeline_id)
        return [PipelineStepSchema.model_validate(pipeline) for pipeline in result]

    async def get_user_pipeline_settings(self, pipeline_id: UUID, user_id: UUID) -> list[PipelineStepSchema]:
        step_pairs = await self._pipeline_step_repo.get_pipeline_steps_with_user_settings(
            pipeline_id=pipeline_id,
            user_id=user_id
        )

        steps_dto: list[PipelineStepSchema] = []
        for step, setting in step_pairs:

            user_settings_dto = None
            if setting is not None:
                user_settings_dto = UserStepSettingsSchema.model_validate(setting)

            step_dto = PipelineStepSchema(
                id=step.id,
                name=step.name,
                display_name=step.display_name,
                agent=step.agent,
                order=step.order,
                system_prompt=step.system_prompt,
                user_prompt=step.user_prompt,
                user_settings=user_settings_dto,
            )
            steps_dto.append(step_dto)

        return steps_dto

    async def cancel_all_user_sessions(self, user_id: UUID) -> None:
        await self._user_pipeline_session_repo.cancel_all_active_sessions(user_id=user_id)


    async def create_user_session(self, user_id: UUID, pipeline_id: UUID) -> UserPipelineSessionSchema:
        instance = UserPipelineSession(
            user_id=user_id,
            pipeline_id=pipeline_id,
        )
        result = await self._user_pipeline_session_repo.create(instance=instance)
        return UserPipelineSessionSchema.model_validate(result)

    async def update_user_session(self, session: UserPipelineSessionSchema) -> UserPipelineSessionSchema:

        instance = UserPipelineSession(session.model_dump())
        result = self._user_pipeline_session_repo.update(instance=instance)
        return UserPipelineSessionSchema.model_validate(result)
