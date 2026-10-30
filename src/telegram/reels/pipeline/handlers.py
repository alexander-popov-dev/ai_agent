from typing import Annotated

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.application.pipeline.service import PipelineService
from src.application.user.service import UserService

from src.telegram.reels.pipeline.keyboards import pipeline_keyboard
from src.telegram.common.context import save_context
from src.telegram.reels.context import ReelsContext, ReelsAction
from src.telegram.reels.callbacks import ReelsCallback

router = Router(name="reels_pipeline")


@router.message(CommandStart())
@inject
async def show_pipeline_screen_start(
        message: Message,
        user_service: Annotated[UserService, FromDishka()],
        pipeline_service: Annotated[PipelineService, FromDishka()],
        state: FSMContext,
) -> None:

    await render_pipeline_screen(
        target=message,
        user_id=str(message.from_user.id),
        user_service=user_service,
        pipeline_service=pipeline_service,
        state=state,
    )


@router.callback_query(ReelsCallback.filter(F.action == ReelsAction.START))
@inject
async def show_pipeline_screen_back(
        callback: CallbackQuery,
        user_service: Annotated[UserService, FromDishka()],
        pipeline_service: Annotated[PipelineService, FromDishka()],
        state: FSMContext,
) -> None:
    await render_pipeline_screen(
        target=callback,
        user_id=str(callback.from_user.id),
        user_service=user_service,
        pipeline_service=pipeline_service,
        state=state,
    )


async def render_pipeline_screen(
        target: Message | CallbackQuery,
        user_id: str,
        user_service: UserService,
        pipeline_service: PipelineService,
        state: FSMContext,
) -> None:
    await state.clear()

    user = await user_service.get_by_external_id(external_id=user_id)
    pipelines = await pipeline_service.get_pipelines()

    context = ReelsContext(user_id=user.id)

    text = "<b>Выбери пайплайн</b>"
    reply_markup = pipeline_keyboard(pipelines=pipelines)

    if isinstance(target, CallbackQuery):
        await target.answer()
        msg = await target.message.edit_text(text=text, reply_markup=reply_markup)
    else:
        msg = await target.answer(text=text, reply_markup=reply_markup)

    context.idea_message_ids = [msg.message_id]
    await save_context(context=context, state=state)
