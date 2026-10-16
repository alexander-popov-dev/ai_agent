from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.ai.schemas import AIModelScheme
from src.pipelines.reels.enums import Callback


def model_keyboards(models: list[AIModelScheme]):
    kb = InlineKeyboardBuilder()

    for model in models:
        kb.button(
            text=model.display_name,
            callback_data=f"{Callback.MODEL}{model.id}",
        )
    kb.adjust(1)

    return kb.as_markup()
