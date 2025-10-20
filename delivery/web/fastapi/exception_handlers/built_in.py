from fastapi import Request
from fastapi.responses import JSONResponse

from adapters.presenters.response_models.error_response_model import (
    ErrorResponseModel,
)


async def bad_request_exception_handler(_: Request, exc: Exception):
    response = ErrorResponseModel(
        status_code=400, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=400, content=response.model_dump())


async def file_not_found_exception_handler(_: Request, exc: Exception):
    response = ErrorResponseModel(
        status_code=404, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=404, content=response.model_dump())


async def permission_exception_handler(_: Request, exc: Exception):
    response = ErrorResponseModel(
        status_code=403, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=403, content=response.model_dump())


async def not_implemented_exception_handler(_: Request, exc: Exception):
    response = ErrorResponseModel(
        status_code=501, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=501, content=response.model_dump())
