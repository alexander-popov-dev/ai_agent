from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.niche.schemas import NicheScheme
from src.application.pipeline.schemas import PipelineSchema
from src.core.enums import Language
from src.telegram.common.callbacks import CommonCallback
from src.telegram.common.keyboards import add_back_button
from src.telegram.reels.context import ReelsAction


def pipeline_keyboard(pipelines: list[PipelineSchema]):

    builder = InlineKeyboardBuilder()

    for pipeline in pipelines:
        builder.button(
            text=pipeline.name,
            callback_data=CommonCallback(
                action=ReelsAction.SELECT_NICHE,
                object_id=str(pipeline.id),
            ),
        )

    builder.adjust(1)

    return builder.as_markup()

def niche_keyboard(niches: list[NicheScheme]):

    builder = InlineKeyboardBuilder()

    for niche in niches:
        builder.button(
            text=niche.name,
            callback_data=CommonCallback(
                action=ReelsAction.SELECT_LANGUAGE,
                object_id=str(niche.id),
            ),

        )
    builder.adjust(1)

    add_back_button(
        builder=builder,
        callback=CommonCallback(action=ReelsAction.SELECT_PIPELINE)
    )

    return builder.as_markup()


def language_keyboard():

    builder = InlineKeyboardBuilder()

    for lang in Language:
        builder.button(
            text=lang.name,
            callback_data=CommonCallback(
                action=ReelsAction.SELECT_NICHE,
                object_id=lang.name,
            ),
        )

    builder.adjust(1)

    add_back_button(
        builder=builder,
        callback=CommonCallback(action=ReelsAction.SELECT_NICHE)
    )

    return builder.as_markup()
