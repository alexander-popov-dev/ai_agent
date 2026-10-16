from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka.integrations.aiogram import inject

from src.telegram.settings.schemas import SettingsSessionSchema
from src.telegram.settings.model.keyboards import model_keyboards
from src.pipelines.reels.enums import Callback

router = Router()

@router.callback_query(F.data.startswith(Callback.PROVIDER))
@inject
async def model(
        callback: CallbackQuery,
        state: FSMContext,
) -> None:
    settings_session = SettingsSessionSchema.model_validate(await state.get_data())
    provider_id = callback.data.replace(Callback.PROVIDER, '')
    for provider in settings_session.providers:
        if str(provider.id) == provider_id:
            await state.set_data(settings_session.model_dump(mode="json"))
            await callback.message.edit_text(text="Выбери модель")
            await callback.message.edit_reply_markup(reply_markup=model_keyboards(models=provider.models))


