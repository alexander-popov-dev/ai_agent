from html import escape

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from pipelines.reels.enums import Callback
from src.pipelines.reels.service import ReelsService
from src.telegram.reels.idea.keyboards import ideas_keyboard
from src.telegram.reels.story.keyboards import story_keyboard
from src.telegram.reels.fsm_state import ReelsState


router = Router()

@router.callback_query(F.data.startswith(Callback.NICHE))
async def niche_selected(
    callback: CallbackQuery,
    service: ReelsService,
):

    niche = callback.data.split(":")[1]

    ideas = await service.generate_ideas(
        user_id=callback.from_user.id,
        niche=niche,
        ideas_count=10,
    )

    text = "\n\n".join(
        f"💡 <b>Идея {i + 1}</b>\n\n"
        f"<b>📌 Название</b>\n"
        f"{escape(idea.title)}\n\n"
        f"<b>📝 Описание</b>\n"
        f"{escape(idea.description)}"
        for i, idea in enumerate(ideas.ideas)
    )

    await callback.message.edit_text(
        text,
        reply_markup=ideas_keyboard(start_index=0, count=len(ideas.ideas)),
    )

@router.callback_query(F.data == Callback.MORE_IDEAS)
async def more_ideas(callback: CallbackQuery, state: FSMContext):

    await state.set_state(ReelsState.waiting_more_ideas)

    await callback.message.answer(
        "Напишите что изменить."
    )

@router.message(ReelsState.waiting_more_ideas)
async def receive_instruction(
    message: Message,
    service: ReelsService,
    state: FSMContext,
):

    ideas_count = await service.get_ideas_count(user_id=message.from_user.id)

    ideas = await service.generate_more_ideas(
        user_id=message.from_user.id,
        instruction=message.text,
        ideas_count=5,
    )

    await state.clear()

    start = ideas_count

    text = "\n\n".join(
        f"💡 <b>Идея {start + (i + 1)}</b>\n\n"
        f"<b>📌 Название</b>\n"
        f"{escape(idea.title)}\n\n"
        f"<b>📝 Описание</b>\n"
        f"{escape(idea.description)}"
        for i, idea in enumerate(ideas.ideas)
    )

    await message.answer(
        text,
        reply_markup=ideas_keyboard(start_index=start,
        count=len(ideas.ideas)),
    )

@router.callback_query(F.data.startswith(Callback.IDEA))
async def idea_selected(
    callback: CallbackQuery,
    service: ReelsService,
):

    index = int(callback.data.split(":")[1])

    await service.select_idea(
        user_id=callback.from_user.id,
        selected_idea_index=index,
    )

    story = await service.generate_story(
        user_id=callback.from_user.id,
    )

    await callback.message.answer(
        text=story.to_html(),
        reply_markup=story_keyboard(),
    )
