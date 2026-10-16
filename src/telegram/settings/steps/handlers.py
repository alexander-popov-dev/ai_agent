from uuid import UUID

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.application.pipeline.service import PipelineService
from src.telegram.settings.schemas import SettingsSessionSchema
from src.telegram.settings.steps.keyboards import step_keyboards
from src.pipelines.reels.enums import Callback

router = Router()

@router.callback_query(F.data.startswith(Callback.PIPELINE))
@inject
async def steps(
        callback: CallbackQuery,
        pipeline_service: FromDishka[PipelineService],
        state: FSMContext,

) -> None:
    settings_session = SettingsSessionSchema.model_validate(await state.get_data())
    pipeline_id = callback.data.replace(Callback.PIPELINE, '')
    user_steps = await pipeline_service.get_user_pipeline_settings(
        user_id=settings_session.user.id,
        pipeline_id=UUID(hex=pipeline_id),
    )

    settings_session.steps = user_steps
    await state.set_data(settings_session.model_dump(mode="json"))
    await callback.message.edit_text(text="Выбери степ")
    await callback.message.edit_reply_markup(reply_markup=step_keyboards(steps=user_steps))
