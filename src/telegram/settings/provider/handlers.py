from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.application.ai.services import AIProviderService
from src.telegram.settings.provider.keyboards import providers_keyboards
from src.telegram.settings.schemas import SettingsSessionSchema
from src.pipelines.reels.enums import Callback

router = Router()

@router.callback_query(F.data.startswith(Callback.STEP))
@inject
async def provider(
        callback: CallbackQuery,
        ai_service: FromDishka[AIProviderService],
        state: FSMContext,

) -> None:
    settings_session = SettingsSessionSchema.model_validate(await state.get_data())
    step_id = callback.data.replace(Callback.STEP, '')

    providers = await ai_service.get_providers_with_models()
    settings_session.providers = providers
    settings_session.step_id = step_id
    await state.update_data(settings_session.model_dump(mode="json"))

    await callback.message.edit_text(text="Выбери провайдера")
    await callback.message.edit_reply_markup(reply_markup=providers_keyboards(providers=providers))
