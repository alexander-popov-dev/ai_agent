from typing import Annotated

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.application.ai.services import AIService
from src.telegram.pipeline_settings.context import SettingsAction, SettingsScope, SettingsContext
from src.telegram.pipeline_settings.provider.keyboards import providers_keyboards
from src.telegram.common.context import get_context, save_context
from src.telegram.pipeline_settings.callbacks import SettingsCallback

router = Router(name="settings_provider")


@router.callback_query(SettingsCallback.filter(F.action == SettingsAction.SELECT_PROVIDER))
@inject
async def show_provider_screen(
        callback: CallbackQuery,
        ai_service: Annotated[AIService, FromDishka()],
        state: FSMContext,

) -> None:
    await callback.answer()

    context = await get_context(state=state, context_cls=SettingsContext)
    context.action = SettingsAction.SELECT_PROVIDER
    context.provider_id = None
    action = SettingsAction.SELECT_STEP if context.scope == SettingsScope.STEP else SettingsAction.SELECT_ALL_STEPS
    await save_context(context=context, state=state)

    providers = await ai_service.get_providers()

    await callback.message.edit_text(
        text="<b>Выбери провайдер</b>",
        reply_markup=providers_keyboards(providers=providers, action=action)
    )
