from fastapi import Request
from fastapi.responses import JSONResponse

from adapters.dto.responses.generic.errors.error import ErrorOutDto
from adapters.gateways.logging.logger_factory import create_console_json_logger
from application.ports.services.logger import LoggerPort
from delivery.web.fastapi.utils.exception_status_mapper import (
    get_http_status_for_exception,
)

logger: LoggerPort = create_console_json_logger("generic_exception_logger")


async def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    Handles all exceptions by dynamically determining the HTTP status code and log level.
    """
    status_code = get_http_status_for_exception(exc)
    message = str(exc) or exc.__class__.__name__

    if 400 <= status_code < 500:
        logger.warning(message, extra={"status_code": status_code})
    else:
        logger.error(message, extra={"status_code": status_code})

    response = ErrorOutDto(
        status_code=status_code, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=status_code, content=response.model_dump())
