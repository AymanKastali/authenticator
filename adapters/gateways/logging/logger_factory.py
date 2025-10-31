from logging import Logger

from adapters.gateways.logging.json_console_logger import (
    get_json_console_logger,
)
from adapters.gateways.logging.logger import LoggerAdapter
from application.ports.services.logger import LoggerPort


def create_logger_adapter() -> LoggerPort:
    """
    Creates a LoggerPort adapter wrapping the JSON console logger.
    This can be injected anywhere in the application.
    """
    loggerizer: Logger = get_json_console_logger()
    return LoggerAdapter(loggerizer)
