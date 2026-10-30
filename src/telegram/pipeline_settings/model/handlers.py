from typing import Annotated
from uuid import UUID

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.application.ai.services import AIService
from src.telegram.pipeline_settings.context import SettingsAction, SettingsContext
from src.telegram.pipeline_settings.model.keyboards import model_keyboards
from src.telegram.common.context import get_context, save_context
from src.telegram.pipeline_settings.callbacks import SettingsCallback

router = Router(name="settings_model")


@router.callback_query(SettingsCallback.filter(F.action == SettingsAction.SELECT_MODEL))
@inject
async def show_model_screen(
        callback: CallbackQuery,
        callback_data: SettingsCallback,
        ai_service: Annotated[AIService, FromDishka()],
        state: FSMContext,
) -> None:
    await callback.answer()
    context = await get_context(state=state, context_cls=SettingsContext)

    provider_id = UUID(callback_data.object_id)
    models = await ai_service.get_models(provider_id=provider_id)

    context.action = SettingsAction.SELECT_MODEL
    context.provider_id = provider_id
    context.model_id = None
    await save_context(state=state, context=context)

    await callback.message.edit_text(
        text="<b>Выбери модель</b>",
        reply_markup=model_keyboards(models=models)
    )
