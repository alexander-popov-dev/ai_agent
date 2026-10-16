from typing import Annotated

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.application.user.service import UserService

from src.telegram.reels.start.keyboards import niche_keyboard, language_keyboard
from src.telegram.reels.fsm_state import ReelsState

router = Router()

@router.message(CommandStart())
@inject
async def start(
        message: Message,
        user_service: Annotated[UserService, FromDishka()],
        state: FSMContext,
) -> None:
    await state.set_state(ReelsState.waiting_niches)
    user = await user_service.get_by_external_id(external_id=str(message.from_user.id))

    await message.answer(text="<i>Выбери нишу</i>", reply_markup=niche_keyboard(user.niches))

@router.callback_query(F.data.startswith('niche_'))
@inject
async def start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ReelsState.waiting_niches)

    await callback.message.edit_text(text="Выбери язык")
    await callback.message.edit_reply_markup(reply_markup=language_keyboard())
