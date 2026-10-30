import traceback
from typing import Any
from uuid import UUID

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

from src.application.pipeline.models import UserPipelineSession
from src.application.pipeline.repository import UserPipelineSessionRepository
from src.application.pipeline.service import PipelineService
from src.core.enums import Language
from src.pipelines.core.enums import PipelineSessionStatus
from src.pipelines.reels.workflow.decisions import ChooseIdeaDecision, ReviewStoryDecision
from src.pipelines.reels.workflow.graph import build_reels_graph
from src.pipelines.reels.workflow.state import ReelsState
from src.pipelines.reels.workflow.contracts import ReelsWorkflowResponse


class ReelsPipelineService:
    """Application boundary for starting and resuming a persisted Reels graph run."""

    def __init__(
            self,
            checkpointer: BaseCheckpointSaver,
            pipeline_service: PipelineService,
            session: UserPipelineSessionRepository
    ) -> None:
        self._checkpointer = checkpointer
        self._pipeline_service = pipeline_service
        self._session = session

    async def _build_graph(self, user_id: UUID, pipeline_id: UUID) -> CompiledStateGraph:
        pipeline_steps = await self._pipeline_service.get_user_pipeline_settings(user_id=user_id,
                                                                                 pipeline_id=pipeline_id)
        return build_reels_graph(pipeline_steps=pipeline_steps, checkpointer=self._checkpointer)

    async def start(
            self,
            *,
            user_id: UUID,
            pipeline_id: UUID,
            niche: str,
            language: Language,
            ideas_count: int,
    ) -> ReelsWorkflowResponse:
        """Create a business session and run until the first user interrupt."""
        session = await self._session.create(
            instance=UserPipelineSession(
                user_id=user_id,
                pipeline_id=pipeline_id,
                status=PipelineSessionStatus.IN_PROGRESS,
            )
        )
        try:
            graph = await self._build_graph(user_id=user_id, pipeline_id=pipeline_id)
            config = self._config(session.id)
            initial_state = ReelsState(
                user_id=user_id,
                niche=niche,
                language=language,
                ideas_count=ideas_count,
            )
            result = await graph.ainvoke(input=initial_state, config=config)
            await self._finish_if_completed(session, result)
            return self._to_response(session.id, result)
        except Exception as exc:
            await self._mark_failed(session, exc)
            raise

    async def resume(
            self,
            *,
            session_id: UUID,
            user_id: UUID,
            decision: ChooseIdeaDecision | ReviewStoryDecision,
    ) -> ReelsWorkflowResponse:
        """Resume the same graph thread after validating session ownership."""
        session = await self._session.get_by_id(session_id)
        try:
            if session is None or session.user_id != user_id:
                # Do not disclose whether a session owned by another user exists.
                raise ValueError("Pipeline session not found")
            if session.status != PipelineSessionStatus.IN_PROGRESS:
                raise ValueError(f"Pipeline session is not active (status={session.status})")
            graph = await self._build_graph(user_id=user_id, pipeline_id=session.pipeline_id)
            result = await graph.ainvoke(
                input=Command(resume=decision),
                config=self._config(session.id),
            )
            await self._finish_if_completed(session, result)
            return self._to_response(session.id, result)
        except Exception as exc:
            await self._mark_failed(session, exc)
            raise

    @staticmethod
    def _config(session_id: UUID) -> dict[str, dict[str, str]]:
        return {"configurable": {"thread_id": str(session_id)}}

    @staticmethod
    def _to_response(session_id: UUID, result: dict[str, Any]) -> ReelsWorkflowResponse:
        interrupt_events = result.get("__interrupt__", ())
        interrupt_payload = interrupt_events[0].value if interrupt_events else None
        state_data = {key: value for key, value in result.items() if key != "__interrupt__"}
        return ReelsWorkflowResponse(
            session_id=session_id,
            state=ReelsState.model_validate(state_data),
            interrupt=interrupt_payload,
        )

    async def _finish_if_completed(self, session: UserPipelineSession, result: dict[str, Any]) -> None:
        if result.get("__interrupt__"):
            session.status = PipelineSessionStatus.IN_PROGRESS
        else:
            session.status = PipelineSessionStatus.COMPLETED
        await self._session.session.flush()

    async def _mark_failed(self, session: UserPipelineSession, exc: Exception) -> None:
        session.status = PipelineSessionStatus.FAILED
        session.error_message = str(exc)
        session.error_traceback = "".join(traceback.format_exception(exc))
        await self._session.session.flush()
