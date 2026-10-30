from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.telegram.reels.context import ReelsAction
from src.telegram.reels.callbacks import ReelsCallback


def story_keyboard():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="✏️ Изменить",
        callback_data=ReelsCallback(
            action=ReelsAction.EDIT_STORY
        ),
    )

    return builder.as_markup()