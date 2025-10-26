from logging import Logger

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from adapters.dto.response_dto.error_response_model import (
    ErrorResponseModel,
)
from adapters.gateways.logging.json_console_logger import (
    get_json_console_logger,
)

logger: Logger = get_json_console_logger("http_exception_logger")


async def http_exception_handler(_: Request, exc: Exception):
    if isinstance(exc, StarletteHTTPException):
        status_code = exc.status_code
        error_name = exc.__class__.__name__
        details = exc.detail
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
