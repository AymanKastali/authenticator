from logging import Logger

from fastapi import Request
from fastapi.responses import JSONResponse

from adapters.dto.response_dto.error_response_model import (
    ErrorResponseModel,
)
from adapters.gateways.logging.json_console_logger import (
    get_json_console_logger,
)
from domain.exceptions.domain_exceptions import DomainError

CUSTOM_ARCHITECTURE_EXCEPTIONS = DomainError

logger: Logger = get_json_console_logger("architecture_exception_logger")


async def architecture_exception_handler(_: Request, exc: Exception):
    """
    Handles all custom exceptions (Domain, Application, Adapter, Delivery)
    which follow the pattern of having status_code, title, and details.
    """
    if isinstance(exc, CUSTOM_ARCHITECTURE_EXCEPTIONS):
        exc_dict = exc.to_dict()
        status_code = exc_dict.get("status_code", 500)
        error_name = exc_dict.get("error", exc.__class__.__name__)
        details = exc_dict.get("details", str(exc))
    else:
        status_code = 500
        error_name = exc.__class__.__name__
        details = str(exc)

    logger.exception(exc, extra={"status_code": status_code})

    response_model = ErrorResponseModel(
        status_code=status_code, error=error_name, details=details
    )
    return JSONResponse(
        status_code=status_code, content=response_model.model_dump()
    )
