from logging import Logger

from fastapi import Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from adapters.dto.response_dto.error_response_model import ErrorResponseModel
from adapters.gateways.logging.json_console_logger import (
    get_json_console_logger,
)
from delivery.web.fastapi.utils.exception_status_mapper import (
    get_http_status_for_exception,
)

VALIDATION_EXCEPTIONS = (RequestValidationError, ValidationError)

logger: Logger = get_json_console_logger("validation_errors_logger")


async def validation_exception_handler(
    _: Request, exc: Exception
) -> JSONResponse:
    if isinstance(exc, VALIDATION_EXCEPTIONS):
        details = exc.errors() if hasattr(exc, "errors") else str(exc)
    else:
        details = str(exc) or "Internal server error"

    status_code = get_http_status_for_exception(exc)

    logger.error(exc)

    response = ErrorResponseModel(
        status_code=status_code, error=exc.__class__.__name__, details=details
    )
    return JSONResponse(status_code=status_code, content=response.model_dump())


async def response_validation_handler(
    _: Request, exc: Exception
) -> JSONResponse:
    """
    Handles ResponseValidationError (500 Internal Server Error).
    """
    status_code = get_http_status_for_exception(exc)
    details = (
        exc.errors()
        if isinstance(exc, ResponseValidationError) and hasattr(exc, "errors")
        else str(exc)
    )
    logger.exception(exc, extra={"status_code": status_code})

    response = ErrorResponseModel(
        status_code=status_code, error=exc.__class__.__name__, details=details
    )
    return JSONResponse(status_code=status_code, content=response.model_dump())
