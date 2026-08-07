from abc import abstractmethod, ABC
from pathlib import Path
from typing import TypeVar

import yaml

from src.core.logging.mixin import LoggedMixin

TOutput = TypeVar(name="TOutput")


class BaseLoader[TOutput](ABC, LoggedMixin):
    __log_layer__ = "loader"

    @staticmethod
    def load_yaml(path: Path) -> dict:
        with open(file=path, mode="r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    @classmethod
    @abstractmethod
    def load(cls, path: Path | str | None = None) -> TOutput:
        ...
