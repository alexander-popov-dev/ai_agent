from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.telegram.keyboards.niche import niche_keyboard

router = Router()

@router.message(CommandStart())
async def start(message: Message):

    await message.answer(
        "<i>Выберите нишу</i>",
        reply_markup=niche_keyboard(),
    )