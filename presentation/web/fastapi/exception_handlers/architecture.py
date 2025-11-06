from fastapi import Request
from fastapi.responses import JSONResponse

from application.ports.services.logger import LoggerPort
from domain.exceptions.domain_errors import DomainError
from infrastructure.exceptions.adapters_errors import AdaptersError
from infrastructure.gateways.logging.factory import (
    create_console_json_logger,
)
from presentation.web.fastapi.schemas.response.generic.errors.error import (
    ErrorResponseSchema,
)
from presentation.web.fastapi.utils.exception_status_mapper import (
    get_http_status_for_exception,
)

CUSTOM_ARCHITECTURE_EXCEPTIONS = (DomainError, AdaptersError)

logger: LoggerPort = create_console_json_logger("architecture_errors_logger")


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

    response_model = ErrorResponseSchema(
        status_code=status_code, error=error_name, details=details
    )
    return JSONResponse(
        status_code=status_code, content=response_model.model_dump()
    )
