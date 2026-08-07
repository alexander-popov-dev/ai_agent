from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.telegram.enums import Callback


def ideas_keyboard(start_index: int, count: int):

    kb = InlineKeyboardBuilder()

    for i in range(start_index, start_index + count):
        kb.button(
            text=str(i + 1),
            callback_data=f"{Callback.IDEA}:{i}",
        )

    kb.button(
        text="➕ Еще идеи",
        callback_data=Callback.MORE_IDEAS,
    ).adjust(3)

    return kb.as_markup()