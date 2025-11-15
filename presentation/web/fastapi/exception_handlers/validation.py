from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from application.ports.services.logger import LoggerPort
from infrastructure.gateways.logging.factory import (
    create_console_json_logger,
)
from presentation.web.fastapi.schemas.response.generic.errors.error import (
    ErrorResponseSchema,
)
from presentation.web.fastapi.utils.exception_status_mapper import (
    get_http_status_for_exception,
)

VALIDATION_EXCEPTIONS = (RequestValidationError, ValidationError)

logger: LoggerPort = create_console_json_logger("validation_errors_logger")

SENSITIVE_FIELDS: set[str] = {
    "secret_key",
    "private_key",
    "public_key",
    "password",
    "token",
}


def redact_sensitive(data: Any) -> Any:
    """
    Recursively replace sensitive fields in a dict or list with 'HIDDEN'.
    """
    if isinstance(data, dict):
        return {
            k: ("HIDDEN" if k in SENSITIVE_FIELDS else redact_sensitive(v))
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [redact_sensitive(v) for v in data]
    return data


async def validation_exception_handler(
    _: Request, exc: Exception
) -> JSONResponse:
    if isinstance(exc, (RequestValidationError, ValidationError)):
        raw_details = exc.errors() if hasattr(exc, "errors") else []
        details = []
        for err in raw_details:
            safe_err = dict(err)
            if "input" in safe_err:
                safe_err["input"] = redact_sensitive(safe_err["input"])
            details.append(safe_err)
    else:
        details = str(exc) or "Internal server error"

    status_code = get_http_status_for_exception(exc)
    logger.error("Validation error occurred", extra={"error": str(exc)})

    response = ErrorResponseSchema(
        status_code=status_code,
        error=exc.__class__.__name__,
        details=details,
    )
    return JSONResponse(status_code=status_code, content=response.model_dump())


# async def validation_exception_handler(
#     _: Request, exc: Exception
# ) -> JSONResponse:
#     if isinstance(exc, VALIDATION_EXCEPTIONS):
#         details = exc.errors() if hasattr(exc, "errors") else str(exc)
#     else:
#         details = str(exc) or "Internal server error"

#     status_code = get_http_status_for_exception(exc)

#     logger.error(exc)

#     response = ErrorResponseSchema(
#         status_code=status_code, error=exc.__class__.__name__, details=details
#     )
#     return JSONResponse(status_code=status_code, content=response.model_dump())


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

    response = ErrorResponseSchema(
        status_code=status_code, error=exc.__class__.__name__, details=details
    )
    return JSONResponse(status_code=status_code, content=response.model_dump())
