from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="🚀 Запустить бота / Главное меню"),
        BotCommand(command="settings", description="🔧 Настройки"),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())