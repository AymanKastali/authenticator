from http.client import HTTPException as HTTPClientException

from fastapi import FastAPI
from fastapi.exceptions import (
    RequestValidationError,
    ResponseValidationError,
)
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from domain.exceptions.domain_errors import (
    DomainError,
    DomainRuleViolationError,
)
from infrastructure.exceptions.adapters_errors import (
    AdaptersError,
    DatabaseConnectionError,
    JwtExpiredError,
    JwtInvalidError,
)
from presentation.web.fastapi.exception_handlers.architecture import (
    architecture_exception_handler,
)
from presentation.web.fastapi.exception_handlers.generic import (
    generic_exception_handler,
)
from presentation.web.fastapi.exception_handlers.http import (
    http_exception_handler,
)
from presentation.web.fastapi.exception_handlers.validation import (
    response_validation_handler,
    validation_exception_handler,
)

EXCEPTION_HANDLERS = {
    # 1. Adapter errors
    JwtExpiredError: http_exception_handler,  # 401 → could use custom handler if needed
    JwtInvalidError: http_exception_handler,  # 401
    DatabaseConnectionError: generic_exception_handler,  # 500
    AdaptersError: architecture_exception_handler,  # 400 fallback
    # 2. Domain errors
    DomainRuleViolationError: architecture_exception_handler,  # 403
    DomainError: architecture_exception_handler,  # 400 fallback
    # 3. Validation errors
    ValidationError: validation_exception_handler,  # 422
    RequestValidationError: validation_exception_handler,  # 422
    ResponseValidationError: response_validation_handler,  # 500
    # 4. Delivery / HTTP errors
    HTTPClientException: http_exception_handler,  # 500
    StarletteHTTPException: http_exception_handler,  # 500
    # 5. Standard Python exceptions (client errors first)
    ValueError: generic_exception_handler,  # 400
    TypeError: generic_exception_handler,  # 400
    KeyError: generic_exception_handler,  # 400
    IndexError: generic_exception_handler,  # 400
    PermissionError: generic_exception_handler,  # 403
    FileNotFoundError: generic_exception_handler,  # 404
    NotImplementedError: generic_exception_handler,  # 501
    ZeroDivisionError: generic_exception_handler,  # 500
    AttributeError: generic_exception_handler,  # 500
    # 6. Generic fallback
    Exception: generic_exception_handler,  # 500
}


def register_exception_handlers(app: FastAPI):
    """
    Register all exception handlers from EXCEPTION_HANDLERS to the FastAPI app.
    """
    for exc_type, handler in EXCEPTION_HANDLERS.items():
        app.add_exception_handler(exc_type, handler)
