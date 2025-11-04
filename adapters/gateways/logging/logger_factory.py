from logging import Logger

from loggerizer.enums import LogField
from loggerizer.loggers import LoggerFactory

from adapters.gateways.logging.logger import LoggerAdapter
from application.ports.services.logger import LoggerPort


def _build_raw_console_json_logger(
    name: str = "authorizer_json_console_logger",
) -> Logger:
    extra_fields: list[LogField] = [
        LogField.CREATED,
        LogField.LEVEL_NO,
        LogField.FILE_NAME,
        LogField.LINE_NO,
        LogField.PATH_NAME,
        LogField.EXCEPTION,
    ]

    return LoggerFactory.json_console_logger(
        name=name, extra_fields=extra_fields
    )


def create_console_json_logger(name: str | None = None) -> LoggerPort:
    """
    Creates a LoggerPort adapter wrapping the JSON console logger.
    This can be injected anywhere in the application.
    """
    loggerizer: Logger
    if name is not None:
        loggerizer = _build_raw_console_json_logger(name=name)
    else:
        loggerizer = _build_raw_console_json_logger()
    return LoggerAdapter(loggerizer)
