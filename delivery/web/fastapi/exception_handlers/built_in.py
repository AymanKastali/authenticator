from logging import Logger

from fastapi import Request
from fastapi.responses import JSONResponse

from adapters.dto.response_dto.error_response_model import (
    ErrorResponseModel,
)
from adapters.gateways.logging.json_console_logger import (
    get_json_console_logger,
)

logger: Logger = get_json_console_logger("builtin_exception_logger")


async def bad_request_exception_handler(_: Request, exc: Exception):
    status_code: int = 400
    logger.warning(exc, extra={"status_code": status_code})
    response = ErrorResponseModel(
        status_code=status_code, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=400, content=response.model_dump())


async def file_not_found_exception_handler(_: Request, exc: Exception):
    status_code: int = 404
    logger.warning(exc, extra={"status_code": status_code})
    response = ErrorResponseModel(
        status_code=status_code, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=404, content=response.model_dump())


async def permission_exception_handler(_: Request, exc: Exception):
    status_code: int = 403
    logger.warning(exc, extra={"status_code": status_code})
    response = ErrorResponseModel(
        status_code=status_code, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=403, content=response.model_dump())


async def not_implemented_exception_handler(_: Request, exc: Exception):
    status_code: int = 501
    logger.error(exc, extra={"status_code": status_code})
    response = ErrorResponseModel(
        status_code=status_code, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=501, content=response.model_dump())
