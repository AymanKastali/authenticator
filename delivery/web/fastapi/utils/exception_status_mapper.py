from http.client import HTTPException as HTTPClientException
from typing import Type

from fastapi.exceptions import RequestValidationError, ResponseValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from adapters.exceptions.adapters_errors import (
    AdaptersError,
    DatabaseConnectionError,
    JWTExpiredError,
    JWTInvalidError,
)
from domain.exceptions.domain_errors import (
    DomainError,
    DomainRuleViolationError,
)

EXCEPTION_STATUS_MAP: dict[Type[Exception], int] = {
    # 1. Adapter errors
    JWTExpiredError: 401,
    JWTInvalidError: 401,
    DatabaseConnectionError: 500,
    AdaptersError: 400,  # fallback for generic adapter errors
    # 2. Domain errors
    DomainRuleViolationError: 403,
    DomainError: 400,  # fallback for generic domain errors
    # 3. Validation errors
    RequestValidationError: 422,
    ResponseValidationError: 500,
    # Pydantic base validation error
    ValidationError: 422,
    # 4. Delivery / HTTP errors
    HTTPClientException: 500,
    StarletteHTTPException: 500,
    # 5. Standard Python exceptions (client errors first)
    ValueError: 400,
    TypeError: 400,
    KeyError: 400,
    IndexError: 400,
    ZeroDivisionError: 500,
    PermissionError: 403,
    FileNotFoundError: 404,
    NotImplementedError: 501,
    AttributeError: 500,
    # 6. Generic fallback
    Exception: 500,
}


def get_http_status_for_exception(exc: Exception) -> int:
    """
    Map any exception to an HTTP status code.
    Uses the EXCEPTION_STATUS_MAP and supports subclass checks.
    Fallbacks to 500 for unknown exceptions.
    """
    if hasattr(exc, "status_code"):
        return getattr(exc, "status_code")

    for exc_type, status in EXCEPTION_STATUS_MAP.items():
        if isinstance(exc, exc_type):
            return status

    return 500
