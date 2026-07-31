import logging
import sys

import structlog

from src.core.settings import get_core_settings


def configure_logging() -> None:
    settings = get_core_settings()

    logging.basicConfig(
        level=settings.log_level,
        stream=sys.stdout,
        format="%(message)s",
    )

    renderer = (
        structlog.processors.JSONRenderer()
        if settings.log_json
        else structlog.dev.ConsoleRenderer(
            colors=settings.debug
        )
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )