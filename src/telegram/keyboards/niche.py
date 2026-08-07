from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.telegram.enums import Callback


def niche_keyboard():

    kb = InlineKeyboardBuilder()

    for niche in [
        "Патентный поверенный",
        "Истории патентования",
        "Факты патентования",
        "Философия патентования",
        "Торговый марки",
        "Авторское право",
        "Защита прав ИС",
        "Факты по Python",
    ]:

        kb.button(
            text=niche,
            callback_data=f"{Callback.NICHE}:{niche}",

        )
        kb.adjust(1)
    return kb.as_markup()