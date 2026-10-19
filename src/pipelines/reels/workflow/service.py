import traceback
from typing import Any
from uuid import UUID

from langgraph.types import Command

from src.application.pipeline.models import UserPipelineSession
from src.application.pipeline.repository import UserPipelineSessionRepository
from src.pipelines.core.enums import PipelineSessionStatus
from src.pipelines.reels.workflow.decisions import ChooseIdeaDecision, ReviewStoryDecision
from src.pipelines.reels.workflow.state import ReelsState
from src.pipelines.reels.workflow.contracts import ReelsWorkflowResponse


class ReelsWorkflowService:
    """Application boundary for starting and resuming a persisted Reels graph run."""

    def __init__(self, graph: Any, sessions: UserPipelineSessionRepository) -> None:
        self._graph = graph
        self._sessions = sessions

    async def start(
        self,
        *,
        user_id: UUID,
        pipeline_id: UUID,
        niche: str,
        language: str = "ua",
        ideas_count: int = 10,
    ) -> ReelsWorkflowResponse:
        """Create a business session and run until the first user interrupt."""
        session = await self._sessions.create(
            instance=UserPipelineSession(
                user_id=user_id,
                pipeline_id=pipeline_id,
                status=PipelineSessionStatus.IN_PROGRESS,
            )
        )
        config = self._config(session.id)
        initial_state = ReelsState(
            user_id=user_id,
            niche=niche,
            language=language,
            ideas_count=ideas_count,
        )

        try:
            result = await self._graph.ainvoke(initial_state.model_dump(mode="json"), config=config)
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
        session = await self._sessions.get_by_id(session_id)
        if session is None or session.user_id != user_id:
            # Do not disclose whether a session owned by another user exists.
            raise ValueError("Pipeline session not found")
        if session.status != PipelineSessionStatus.IN_PROGRESS:
            raise ValueError(f"Pipeline session is not active (status={session.status})")

        try:
            result = await self._graph.ainvoke(
                Command(resume=decision.model_dump(mode="json")),
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
        await self._sessions.session.flush()

    async def _mark_failed(self, session: UserPipelineSession, exc: Exception) -> None:
        session.status = PipelineSessionStatus.FAILED
        session.error_message = str(exc)
        session.error_traceback = "".join(traceback.format_exception(exc))
        await self._sessions.session.flush()
