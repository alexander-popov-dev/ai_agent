from uuid import UUID

from src.application.ai.schemas import AIModelWithProviderSchema, AIProviderSchema
from src.application.pipeline.models import UserPipelineSession
from src.application.pipeline.repository import (
    PipelineRepository,
    PipelineStepRepository,
    UserPipelineSettingsRepository, UserPipelineSessionRepository
)
from src.application.pipeline.schemas import PipelineSchema, PipelineStepSchema, UserStepSettingsSchema, \
    UserPipelineSessionSchema, UserStepSettingsUpdateSchema, UserStepSettingsWithModelSchema, \
    PipelineStepWithUserSettingsSchema


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

    async def get_pipelines(self) -> list[PipelineSchema]:
        result = await self._pipeline_repo.get_all()
        return [PipelineSchema.model_validate(pipeline) for pipeline in result if pipeline.is_active]

    async def get_pipeline_steps(self, pipeline_id: UUID) -> list[PipelineStepSchema]:
        result = await self._pipeline_step_repo.get_pipline_steps(pipeline_id=pipeline_id)
        return [PipelineStepSchema.model_validate(pipeline) for pipeline in result]

    async def get_user_pipline_step(self, step_id: UUID, user_id: UUID) -> UserStepSettingsSchema:
        result = await self._user_pipeline_settings_repo.get_user_pipline_step(step_id=step_id, user_id=user_id)
        return UserStepSettingsSchema.model_validate(result)

    async def get_user_pipeline_settings(self, pipeline_id: UUID, user_id: UUID) -> list[PipelineStepWithUserSettingsSchema]:
        rows = await self._pipeline_step_repo.get_pipeline_steps_with_user_settings(
            pipeline_id=pipeline_id,
            user_id=user_id,
        )

        result = []
        for step, settings, model, provider in rows:
            user_settings = None
            if settings is not None:
                provider = AIProviderSchema.model_validate(provider)

                model = AIModelWithProviderSchema(
                    id=model.id,
                    name=model.name,
                    display_name=model.display_name,
                    provider=provider,
                )

                user_settings = UserStepSettingsWithModelSchema(
                    id=settings.id,
                    user_id=settings.user_id,
                    step_id=settings.step_id,
                    temperature=settings.temperature,
                    model=model,
                )

            result.append(
                PipelineStepWithUserSettingsSchema(
                    id=step.id,
                    name=step.name,
                    display_name=step.display_name,
                    agent=step.agent,
                    order=step.order,
                    system_prompt=step.system_prompt,
                    user_prompt=step.user_prompt,
                    user_settings=user_settings,
                )
            )
        return result

    async def upsert_settings(self, settings: list[UserStepSettingsUpdateSchema]) -> None:
        await self._user_pipeline_settings_repo.upsert_for_steps(
            settings=[setting.model_dump(exclude_unset=True) for setting in settings]
        )

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
        result = await self._user_pipeline_session_repo.update(instance=instance)
        return UserPipelineSessionSchema.model_validate(result)
