from aiogram.filters.callback_data import CallbackData


class SettingsCallback(CallbackData, prefix="settings"):
    action: str
    object_id: str | int | None = None