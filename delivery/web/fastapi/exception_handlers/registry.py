from http.client import HTTPException

from fastapi.exceptions import (
    RequestValidationError,
    ResponseValidationError,
)
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from delivery.web.fastapi.exception_handlers.architecture import (
    architecture_exception_handler,
)
from delivery.web.fastapi.exception_handlers.built_in import (
    bad_request_exception_handler,
    file_not_found_exception_handler,
    not_implemented_exception_handler,
    permission_exception_handler,
)
from delivery.web.fastapi.exception_handlers.http import (
    http_exception_handler,
)
from delivery.web.fastapi.exception_handlers.internal import (
    internal_server_exception_handler,
)
from delivery.web.fastapi.exception_handlers.validation import (
    response_validation_handler,
    validation_exception_handler,
)
from domain.exceptions.domain_exceptions import DomainError

EXCEPTION_HANDLERS = {
    # Standard Python Exceptions (400)
    ValueError: bad_request_exception_handler,
    TypeError: bad_request_exception_handler,
    KeyError: bad_request_exception_handler,
    IndexError: bad_request_exception_handler,
    ZeroDivisionError: bad_request_exception_handler,
    # Standard Python Exceptions (Other)
    PermissionError: permission_exception_handler,
    FileNotFoundError: file_not_found_exception_handler,
    NotImplementedError: not_implemented_exception_handler,
    AttributeError: internal_server_exception_handler,  # Treat as 500 error
    # Custom Application Exceptions
    DomainError: architecture_exception_handler,
    # FastAPI / Pydantic Exceptions
    HTTPException: http_exception_handler,
    StarletteHTTPException: http_exception_handler,
    ValidationError: validation_exception_handler,
    RequestValidationError: validation_exception_handler,
    ResponseValidationError: response_validation_handler,
    # Generic Fallback (Catches all unhandled Exception types)
    Exception: internal_server_exception_handler,
}
