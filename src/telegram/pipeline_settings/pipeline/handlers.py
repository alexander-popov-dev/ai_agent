from typing import Annotated

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.application.pipeline.service import PipelineService
from src.telegram.pipeline_settings.context import SettingsContext, SettingsAction
from src.telegram.pipeline_settings.pipeline.keyboards import pipeline_keyboard
from src.application.user.service import UserService
from src.telegram.common.context import save_context
from src.telegram.pipeline_settings.callbacks import SettingsCallback

router = Router(name="pipeline")


@router.message(Command("settings"))
@inject
async def show_pipeline_screen(
        message: Message,
        state: FSMContext,
        pipeline_service: Annotated[PipelineService, FromDishka()],
        user_service: Annotated[UserService, FromDishka()],
) -> None:
    await state.clear()

    user = await user_service.get_by_external_id(external_id=str(message.from_user.id))
    pipelines = await pipeline_service.get_pipelines()

    context = SettingsContext(user_id=user.id)
    await save_context(context=context, state=state)

    await message.answer(
        text="<b>Выбери пайплайн</b>",
        reply_markup=pipeline_keyboard(pipelines=pipelines)
    )

@router.callback_query(SettingsCallback.filter(F.action == SettingsAction.START))
@inject
async def show_pipeline_screen(
        callback: CallbackQuery,
        state: FSMContext,
        pipeline_service: Annotated[PipelineService, FromDishka()],
        user_service: Annotated[UserService, FromDishka()],
) -> None:
    await callback.answer()

    await state.clear()

    user = await user_service.get_by_external_id(external_id=str(callback.from_user.id))
    pipelines = await pipeline_service.get_pipelines()

    context = SettingsContext(user_id=user.id)
    await save_context(context=context, state=state)

    await callback.message.edit_text(
        text="Выбери пайплайн",
        reply_markup=pipeline_keyboard(pipelines=pipelines)
    )
