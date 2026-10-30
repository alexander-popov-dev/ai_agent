from uuid import UUID

from sqlalchemy import select, Sequence, and_, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import contains_eager, joinedload

from src.application.ai.models import AIModel, AIProvider
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
    ) -> Sequence[tuple[PipelineStep, UserPipelineSettings, AIModel, AIProvider | None]]:
        statement = (
            select(PipelineStep, UserPipelineSettings, AIModel, AIProvider)
            .outerjoin(
                UserPipelineSettings,
                and_(
                    UserPipelineSettings.step_id == PipelineStep.id,
                    UserPipelineSettings.user_id == user_id,
                ),
            )
            .outerjoin(
                AIModel,
                AIModel.id == UserPipelineSettings.model_id
            )
            .outerjoin(
                AIProvider,
                AIProvider.id == AIModel.provider_id
            )
            .where(
                PipelineStep.pipeline_id == pipeline_id,
                PipelineStep.is_active.is_(True),
            )
            .order_by(PipelineStep.order)
        )
        result = await self.session.execute(statement)
        return list(result.all())


class UserPipelineSettingsRepository(BaseRepository[UserPipelineSettings]):
    model = UserPipelineSettings

    async def get_user_pipline_step(self, step_id: UUID, user_id: UUID) -> UserPipelineSettings | None:
        statement = (
            select(self.model)
            .where(
                and_(
                    self.model.step_id == step_id,
                    self.model.user_id == user_id,
                )
            )
        )
        result = await self.session.execute(statement=statement)
        return result.scalar_one_or_none()

    SETTING_FIELDS = frozenset({
        "model_id",
        "temperature",
    })

    async def upsert_for_steps(self, settings: list) -> None:
        """Insert or update selected settings for one or more steps."""
        update_fields = set(settings[0]) - {"user_id", "step_id"}

        if not update_fields:
            raise ValueError("No settings to update.")

        if any(
                set(record) - {"user_id", "step_id"} != update_fields
                for record in settings
        ):
            raise ValueError(
                "All settings must contain the same fields."
            )

        statement = insert(self.model).values(settings)

        update_values = {
            field: getattr(statement.excluded, field)
            for field in update_fields
        }
        # update_values["updated_at"] = func.now()

        statement = statement.on_conflict_do_update(
            constraint="uq_user_step",
            set_=update_values,
        )

        await self.session.execute(statement)


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
