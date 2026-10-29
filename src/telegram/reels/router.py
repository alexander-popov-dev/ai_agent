from aiogram import Router

from src.telegram.reels.pipeline.handlers import router as pipeline_router
from src.telegram.reels.niche.handlers import router as niche_router
from src.telegram.reels.language.handlers import router as language_router
from src.telegram.reels.idea.handlers import router as idea_router
from src.telegram.reels.story.handlers import router as story_router

router = Router(name="pipeline_reels")

router.include_routers(
    pipeline_router,
    niche_router,
    language_router,
    idea_router,
    story_router,
)
