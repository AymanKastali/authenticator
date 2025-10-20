from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from adapters.presenters.response_models.error_response_model import (
    ErrorResponseModel,
)


async def http_exception_handler(_: Request, exc: Exception):
    if isinstance(exc, StarletteHTTPException):
        response = ErrorResponseModel(
            status_code=exc.status_code,
            error=exc.__class__.__name__,
            details=exc.detail,
        )
        return JSONResponse(
            status_code=exc.status_code, content=response.model_dump()
        )

    response = ErrorResponseModel(
        status_code=500, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=500, content=response.model_dump())
