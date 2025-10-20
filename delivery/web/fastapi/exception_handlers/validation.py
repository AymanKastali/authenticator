from fastapi import Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from adapters.presenters.response_models.error_response_model import (
    ErrorResponseModel,
)

VALIDATION_EXCEPTIONS = (RequestValidationError, ValidationError)


async def validation_exception_handler(_: Request, exc: Exception):
    if isinstance(exc, VALIDATION_EXCEPTIONS):
        details = exc.errors() if hasattr(exc, "errors") else str(exc)
        status = 422

    else:
        details = str(exc) or "Internal server error"
        status = 500

    response = ErrorResponseModel(
        status_code=status,
        error=exc.__class__.__name__,
        details=details,
    )
    return JSONResponse(status_code=status, content=response.model_dump())


async def response_validation_handler(_: Request, exc: Exception):
    """
    Handles ResponseValidationError (500 Internal Server Error).
    """
    # Log as an exception because this is a server bug

    if isinstance(exc, ResponseValidationError):
        details = exc.errors() if hasattr(exc, "errors") else str(exc)
        status_code = 500

        response = ErrorResponseModel(
            status_code=status_code,
            error=exc.__class__.__name__,
            details=details,
        )
        return JSONResponse(
            status_code=status_code, content=response.model_dump()
        )

    response = ErrorResponseModel(
        status_code=500,
        error=exc.__class__.__name__,
        details=str(exc),
    )
    return JSONResponse(status_code=500, content=response.model_dump())
