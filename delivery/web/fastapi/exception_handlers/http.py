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

logger: Logger = get_json_console_logger("http_errors_logger")


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
    response_model = ErrorResponseModel(
        status_code=status_code, error=error_name, details=details
    )

    return JSONResponse(
        status_code=status_code, content=response_model.model_dump()
    )
