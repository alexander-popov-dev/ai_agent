from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka.integrations.aiogram import inject

from src.telegram.pipeline_settings.context import SettingsAction, SettingsScope, SettingsContext
from src.telegram.pipeline_settings.temperature.keyboards import temperature_keyboards
from src.telegram.common.context import get_context, save_context
from src.telegram.pipeline_settings.callbacks import SettingsCallback

router = Router(name="settings_temperature")


@router.callback_query(SettingsCallback.filter(F.action == SettingsAction.SELECT_TEMPERATURE))
@inject
async def show_temperatura_screen(
        callback: CallbackQuery,
        state: FSMContext,
) -> None:
    await callback.answer()
    context = await get_context(state=state, context_cls=SettingsContext)

    context.action = SettingsAction.SELECT_TEMPERATURE
    action = SettingsAction.SELECT_STEP if context.scope == SettingsScope.STEP else SettingsAction.SELECT_ALL_STEPS
    await save_context(state=state, context=context)

    await callback.message.edit_text(
        text="<b>Выбери температуру</b>",
        reply_markup=temperature_keyboards(action=action)
    )
