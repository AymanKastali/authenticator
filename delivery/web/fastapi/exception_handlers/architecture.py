from logging import Logger

from fastapi import Request
from fastapi.responses import JSONResponse

from adapters.dto.responses.generic.errors.error import ErrorOutDto
from adapters.exceptions.adapters_errors import AdaptersError
from adapters.gateways.logging.json_console_logger import (
    get_json_console_logger,
)
from delivery.web.fastapi.utils.exception_status_mapper import (
    get_http_status_for_exception,
)
from domain.exceptions.domain_errors import DomainError

CUSTOM_ARCHITECTURE_EXCEPTIONS = (DomainError, AdaptersError)

logger: Logger = get_json_console_logger("architecture_errors_logger")


async def architecture_exception_handler(
    _: Request, exc: Exception
) -> JSONResponse:
    """
    Handles all custom exceptions (Domain, Application, Adapter, Delivery)
    which follow the pattern of having status_code, title, and details.
    """
    status_code: int = get_http_status_for_exception(exc)

    if isinstance(exc, CUSTOM_ARCHITECTURE_EXCEPTIONS):
        exc_dict = exc.to_dict()
        error_name = exc_dict.get("error", exc.__class__.__name__)
        details = exc_dict.get("details", str(exc))
    else:
        error_name = exc.__class__.__name__
        details = str(exc) or "Internal server error"

    logger.exception(exc)

    response_model = ErrorOutDto(
        status_code=status_code, error=error_name, details=details
    )
    return JSONResponse(
        status_code=status_code, content=response_model.model_dump()
    )
