from typing import Annotated

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.application.pipeline.service import PipelineService
from src.telegram.settings.pipeline.keyboards import pipeline_keyboard
from src.telegram.settings.schemas import SettingsSessionSchema
from src.application.user.service import UserService

router = Router()


@router.message(Command("settings"))
@inject
async def pipeline(
        message: Message,
        pipeline_service: Annotated[PipelineService, FromDishka()],
        user_service: Annotated[UserService, FromDishka()],
        state: FSMContext,
) -> None:
    user = await user_service.get_by_external_id(external_id=str(message.chat.id))
    pipelines = await pipeline_service.get_pipelines()

    settings_session = SettingsSessionSchema(user=user)
    await state.update_data(settings_session.model_dump(mode="json"))

    await message.answer(
        text="<i>Выбери пайплайн</i>",
        reply_markup=pipeline_keyboard(pipelines=pipelines)
    )
