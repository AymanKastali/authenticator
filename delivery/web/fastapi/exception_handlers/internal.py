from fastapi import Request
from fastapi.responses import JSONResponse

from adapters.presenters.response_models.error_response_model import (
    ErrorResponseModel,
)


async def internal_server_exception_handler(_: Request, exc: Exception):
    response = ErrorResponseModel(
        status_code=500, error=exc.__class__.__name__, details=str(exc)
    )
    return JSONResponse(status_code=500, content=response.model_dump())
