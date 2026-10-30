from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core.enums import Language
from src.telegram.common.keyboards import add_back_button
from src.telegram.reels.context import ReelsAction
from src.telegram.reels.callbacks import ReelsCallback


def language_keyboard():
    builder = InlineKeyboardBuilder()

    for lang in Language:
        builder.button(
            text=lang.name,
            callback_data=ReelsCallback(
                action=ReelsAction.SELECT_LANGUAGE,
                object_id=lang.value,
            ),
        )

    builder.adjust(1)

    add_back_button(
        builder=builder,
        callback=ReelsCallback(action=ReelsAction.SELECT_PIPELINE)
    )

    return builder.as_markup()
