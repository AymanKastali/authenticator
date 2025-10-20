from fastapi import Request
from fastapi.responses import JSONResponse

from adapters.presenters.response_models.error_response_model import (
    ErrorResponseModel,
)
from domain.exceptions.domain_exceptions import DomainError

CUSTOM_ARCHITECTURE_EXCEPTIONS = DomainError


async def architecture_exception_handler(_: Request, exc: Exception):
    """
    Handles all custom exceptions (Domain, Application, Adapter, Delivery)
    which follow the pattern of having status_code, title, and details.
    """

    if isinstance(exc, CUSTOM_ARCHITECTURE_EXCEPTIONS):
        exc_dict: dict = exc.to_dict()

        response = ErrorResponseModel(
            status_code=exc_dict.get("status_code", 500),
            error=exc_dict.get("error", exc.__class__.__name__),
            details=exc_dict.get("details", str(exc)),
        )

        return JSONResponse(
            status_code=response.status_code,
            content=response.model_dump(),
        )

    response = ErrorResponseModel(
        status_code=500,
        error=exc.__class__.__name__,
        details=str(exc),
    )

    return JSONResponse(status_code=500, content=response.model_dump())
