from logging import Logger

from loggerizer.enums import LogField
from loggerizer.loggers import LoggerFactory


def get_json_console_logger(
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
