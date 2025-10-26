from logging import Logger

from fastapi import Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from adapters.dto.response_dto.error_response_model import (
    ErrorResponseModel,
)
from adapters.gateways.logging.json_console_logger import (
    get_json_console_logger,
)

VALIDATION_EXCEPTIONS = (RequestValidationError, ValidationError)

logger: Logger = get_json_console_logger("internal_exception_logger")


async def validation_exception_handler(_: Request, exc: Exception):
    if isinstance(exc, VALIDATION_EXCEPTIONS):
        details = exc.errors() if hasattr(exc, "errors") else str(exc)
        status_code = 422
        logger.warning(exc, extra={"status_code": status_code})
    else:
        details = str(exc) or "Internal server error"
        status_code = 500
        logger.error(exc, extra={"status_code": status_code})

    response = ErrorResponseModel(
        status_code=status_code, error=exc.__class__.__name__, details=details
    )
    return JSONResponse(status_code=status_code, content=response.model_dump())


async def response_validation_handler(_: Request, exc: Exception):
    """
    Handles ResponseValidationError (500 Internal Server Error).
    """
    status_code = 500
    details = (
        exc.errors()
        if isinstance(exc, ResponseValidationError) and hasattr(exc, "errors")
        else str(exc)
    )
    logger.exception(exc, extra={"status_code": status_code})

    response = ErrorResponseModel(
        status_code=status_code, error=exc.__class__.__name__, details=details
    )
    return JSONResponse(status_code=500, content=response.model_dump())
