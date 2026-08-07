# telegram/router.py
from aiogram.dispatcher import router
from src.telegram.handlers.start import router as start_router
from src.telegram.handlers.ideas import router as ideas_router
from src.telegram.handlers.story import router as story_router

router.include_router(start_router)
router.include_router(ideas_router)
router.include_router(story_router)