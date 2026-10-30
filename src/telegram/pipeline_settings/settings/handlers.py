from uuid import UUID

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka.integrations.aiogram import inject

from src.telegram.pipeline_settings.context import SettingsAction, SettingsScope, SettingsContext
from src.telegram.pipeline_settings.settings.keyboards import settings_keyboards
from src.telegram.common.context import get_context, save_context
from src.telegram.pipeline_settings.callbacks import SettingsCallback

router = Router(name="settings_setting")


@router.callback_query(
    SettingsCallback.filter(F.action.in_([SettingsAction.SELECT_STEP, SettingsAction.SELECT_ALL_STEPS])))
@inject
async def show_settings_screen(
        callback: CallbackQuery,
        callback_data: SettingsCallback,
        state: FSMContext,
) -> None:
    await callback.answer()
    context = await get_context(state=state, context_cls=SettingsContext)
    step_id = callback_data.object_id

    if step_id:
        step_id = UUID(step_id)
        context.step_id = step_id

    if callback_data.action == SettingsAction.SELECT_STEP:
        context.scope = SettingsScope.STEP
    else:
        context.scope = SettingsScope.PIPELINE
        context.step_id = None

    context.action = SettingsAction.SELECT_SETTINGS
    context.provider_id = None
    context.model_id = None

    await save_context(context=context, state=state)

    await callback.message.edit_text(
        text="<b>Выбери параметр</b>",
        reply_markup=settings_keyboards()
    )

