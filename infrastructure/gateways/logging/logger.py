from logging import Logger
from typing import Mapping

from application.ports.services.logger import LoggerPort


class LoggerAdapter(LoggerPort):
    """
    Adapter implementing LoggerPort using an existing Python Logger.
    Wraps get_json_console_logger() for structured logging.
    """

    def __init__(self, logger: Logger):
        self._logger = logger
        # self._logger = logger or create_console_json_logger()

    def debug(
        self, message: object, extra: Mapping[str, object] | None = None
    ) -> None:
        self._logger.debug(message, extra=extra)

    def info(
        self, message: object, extra: Mapping[str, object] | None = None
    ) -> None:
        self._logger.info(message, extra=extra)

    def warning(
        self, message: object, extra: Mapping[str, object] | None = None
    ) -> None:
        self._logger.warning(message, extra=extra)

    def error(
        self, message: object, extra: Mapping[str, object] | None = None
    ) -> None:
        self._logger.error(message, extra=extra)

    def exception(
        self, message: object, extra: Mapping[str, object] | None = None
    ) -> None:
        """
        Logs an error message with exception context.
        """
        self._logger.exception(message, extra=extra)
