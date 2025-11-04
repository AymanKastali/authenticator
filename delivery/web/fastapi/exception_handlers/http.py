from fastapi import Request
from fastapi.responses import JSONResponse

from adapters.dto.responses.generic.errors.error import ErrorOutDto
from adapters.gateways.logging.logger_factory import create_console_json_logger
from application.ports.services.logger import LoggerPort
from delivery.web.fastapi.utils.exception_status_mapper import (
    get_http_status_for_exception,
)

logger: LoggerPort = create_console_json_logger("http_errors_logger")


async def http_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    Handles HTTP-related exceptions and maps them to appropriate status codes
    using get_http_status_for_exception.
    """
    status_code = get_http_status_for_exception(exc)
    error_name = exc.__class__.__name__
    details = str(exc) if str(exc) else error_name

    # Log the exception with the resolved status code
    logger.exception(exc, extra={"status_code": status_code})

    # Build response
    response_model = ErrorOutDto(
        status_code=status_code, error=error_name, details=details
    )

    return JSONResponse(
        status_code=status_code, content=response_model.model_dump()
    )
