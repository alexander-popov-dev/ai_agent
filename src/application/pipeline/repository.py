from uuid import UUID

from sqlalchemy import select, Sequence, and_, update, or_

from src.application.pipeline.models import Pipeline, PipelineStep, UserPipelineSettings, UserPipelineSession
from src.database.postgres.repository import BaseRepository
from src.pipelines.core.enums import PipelineSessionStatus


class PipelineRepository(BaseRepository[Pipeline]):
    model = Pipeline


class PipelineStepRepository(BaseRepository[PipelineStep]):
    model = PipelineStep

    async def get_pipline_steps(self, pipeline_id: UUID) -> Sequence[PipelineStep]:
        statement = (
            select(self.model)
            .where(
                and_(
                    self.model.pipeline_id == pipeline_id,
                    self.model.is_active.is_(True),
                )
            )
            .order_by(self.model.order)
        )
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def get_pipeline_steps_with_user_settings(
            self,
            pipeline_id: UUID,
            user_id: UUID
    ) -> Sequence[tuple[PipelineStep, UserPipelineSettings | None]]:
        statement = (
            select(PipelineStep, UserPipelineSettings)
            .outerjoin(
                UserPipelineSettings,
                and_(
                    UserPipelineSettings.step_id == PipelineStep.id,
                    UserPipelineSettings.user_id == user_id,
                )
            )
            .where(
                PipelineStep.pipeline_id == pipeline_id,
                PipelineStep.is_active.is_(True),
            )
            .order_by(PipelineStep.order)
        )

        result = await self.session.execute(statement)
        return result.all()


class UserPipelineSettingsRepository(BaseRepository[UserPipelineSettings]):
    model = UserPipelineSettings


class UserPipelineSessionRepository(BaseRepository[UserPipelineSession]):
    model = UserPipelineSession

    async def get_active_session(self, user_id: UUID, pipeline_id: UUID) -> UserPipelineSession | None:
        statement = select(self.model).where(
            self.model.user_id == user_id,
            self.model.pipeline_id == pipeline_id,
            self.model.status == PipelineSessionStatus.IN_PROGRESS,
        )
        res = await self.session.execute(statement)
        return res.scalar_one_or_none()

    async def cancel_all_active_sessions(self, user_id: UUID) -> None:
        statement = (
            update(self.model)
            .where(
                self.model.user_id == user_id,
                self.model.status.in_([
                    PipelineSessionStatus.CREATED,
                    PipelineSessionStatus.IN_PROGRESS
                ])
            )
            .values(status=PipelineSessionStatus.CANCELED)
        )
        await self.session.execute(statement=statement)
