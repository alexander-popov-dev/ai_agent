from functools import cached_property

from src.core.logging.logger import get_logger


class LoggedMixin:
    __log_layer__: str | None = None

    @cached_property
    def logger(self):
        context = {
            "component": self.__class__.__name__,
        }

        if self.__log_layer__:
            context["layer"] = self.__log_layer__

        return get_logger().bind(**context)