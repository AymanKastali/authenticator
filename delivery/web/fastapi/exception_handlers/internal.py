from logging import Logger

from fastapi import Request
from fastapi.responses import JSONResponse

from adapters.dto.response_dto.error_response_model import (
    ErrorResponseModel,
)
from adapters.gateways.logging.json_console_logger import (
    get_json_console_logger,
)

logger: Logger = get_json_console_logger("internal_exception_logger")


async def internal_server_exception_handler(_: Request, exc: Exception):
    status_code: int = 500
    logger.error(exc, extra={"status_code": status_code})
    response = ErrorResponseModel(
        status_code=status_code, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=500, content=response.model_dump())
