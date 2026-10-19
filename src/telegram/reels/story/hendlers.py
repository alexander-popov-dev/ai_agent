from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from pipelines.reels.enums import Callback
from src.pipelines.reels.service import ReelsService
from src.telegram.reels.story.keyboards import story_keyboard
from src.telegram.reels.fsm_state import ReelsState

router = Router()


@router.callback_query(F.data == Callback.EDIT_STORY)
async def edit_story(callback: CallbackQuery, state: FSMContext):

    await state.set_state(ReelsState.waiting_story_edit)

    await callback.message.answer(
        "Что изменить?"
    )


@router.message(ReelsState.waiting_story_edit)
async def edit_story_message(
    message: Message,
    service: ReelsService,
    state: FSMContext,
):

    story = await service.edit_story(
        user_id=message.from_user.id,
        instruction=message.text
    )

    await message.answer(
        text=story.to_html(),
        reply_markup=story_keyboard()
    )

    await state.clear()


@router.callback_query(F.data == Callback.APPROVE_STORY)
async def approve_story(
    callback: CallbackQuery,
    service: ReelsService,
):

    await service.approve_story(
        user_id=callback.from_user.id,
    )

    await callback.message.edit_reply_markup()

    await callback.message.answer(
        "🎉 История сохранена."
    )