from aiogram.utils.keyboard import InlineKeyboardBuilder

from pipelines.reels.enums import Callback


def story_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="✏️ Изменить",
        callback_data=Callback.EDIT_STORY,
    )

    kb.button(
        text="✅ Одобрить",
        callback_data=Callback.APPROVE_STORY,
    )

    kb.adjust(2)

    return kb.as_markup()