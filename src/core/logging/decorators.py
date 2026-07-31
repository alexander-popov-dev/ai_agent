import functools
import time

from src.core.logging.logger import get_logger


logger = get_logger()


def log_execution(func):

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):

        start = time.perf_counter()

        logger.info(
            "Started",
            function=func.__qualname__,
        )

        try:
            return await func(*args, **kwargs)

        finally:
            logger.info(
                "Finished",
                function=func.__qualname__,
                duration=round(time.perf_counter() - start, 3),
            )

    return wrapper