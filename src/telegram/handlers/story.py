from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.pipelines.reels.service import ReelsService
from src.telegram.enums import Callback
from src.telegram.keyboards.story import story_keyboard
from src.telegram.state import ReelsStates

router = Router()


@router.callback_query(F.data == Callback.EDIT_STORY)
async def edit_story(callback: CallbackQuery, state: FSMContext):

    await state.set_state(ReelsStates.waiting_story_edit)

    await callback.message.answer(
        "Что изменить?"
    )


@router.message(ReelsStates.waiting_story_edit)
async def edit_story_message(
    message: Message,
    service: ReelsService,
    state: FSMContext,
):

    await service.parse_user_answer(
        user_id=message.from_user.id,
        answer=message.text,
    )

    story = await service.edit_story(
        user_id=message.from_user.id,
    )

    await state.clear()

    messages = story.to_html_messages()

    for index, text in enumerate(messages):

        if index == len(messages) - 1:
            await message.answer(
                text,
                reply_markup=story_keyboard(),
            )
        else:
            await message.answer(text)


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