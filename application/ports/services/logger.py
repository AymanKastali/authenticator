from abc import ABC, abstractmethod
from typing import Mapping


class LoggerPort(ABC):
    @abstractmethod
    def debug(
        self, message: object, extra: Mapping[str, object] | None = None
    ) -> None:
        pass

    @abstractmethod
    def info(
        self, message: object, extra: Mapping[str, object] | None = None
    ) -> None:
        pass

    @abstractmethod
    def warning(
        self, message: object, extra: Mapping[str, object] | None = None
    ) -> None:
        pass

    @abstractmethod
    def error(
        self, message: object, extra: Mapping[str, object] | None = None
    ) -> None:
        pass

    @abstractmethod
    def exception(
        self, message: object, extra: Mapping[str, object] | None = None
    ) -> None:
        pass
