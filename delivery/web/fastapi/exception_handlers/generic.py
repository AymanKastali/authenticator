from logging import Logger

from fastapi import Request
from fastapi.responses import JSONResponse

from adapters.dto.response_dto.error_response_model import ErrorResponseModel
from adapters.gateways.logging.json_console_logger import (
    get_json_console_logger,
)
from delivery.web.fastapi.utils.exception_status_mapper import (
    get_http_status_for_exception,
)

logger: Logger = get_json_console_logger("generic_exception_logger")


async def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    Handles all exceptions by dynamically determining the HTTP status code and log level.
    """
    status_code = get_http_status_for_exception(exc)
    message = str(exc) or exc.__class__.__name__

    # Log as warning for client errors (4xx), error for server errors (5xx)
    if 400 <= status_code < 500:
        logger.warning(message, extra={"status_code": status_code})
    else:
        logger.error(message, extra={"status_code": status_code})

    # Build response
    response = ErrorResponseModel(
        status_code=status_code, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=status_code, content=response.model_dump())
