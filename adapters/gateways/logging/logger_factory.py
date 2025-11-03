from logging import Logger

from adapters.gateways.logging.json_console_logger import (
    get_json_console_logger,
)
from adapters.gateways.logging.logger import LoggerAdapter
from application.ports.services.logger import LoggerPort


def create_console_json_logger(name: str | None = None) -> LoggerPort:
    """
    Creates a LoggerPort adapter wrapping the JSON console logger.
    This can be injected anywhere in the application.
    """
    loggerizer: Logger
    if name is not None:
        loggerizer = get_json_console_logger(name=name)
    else:
        loggerizer = get_json_console_logger()
    return LoggerAdapter(loggerizer)
