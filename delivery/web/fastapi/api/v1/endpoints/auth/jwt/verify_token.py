from typing import Annotated

from fastapi import Depends, Request

from adapters.dto.requests.auth.jwt.verify_token import VerifyJwtTokenInDto
from delivery.web.fastapi.api.v1.dependencies.jwt import (
    verify_jwt_token_handler_dependency,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.verify_token import (
    VerifyJwtTokenHandler,
)


async def verify_jwt_token_endpoint(
    _request: Request,
    body: VerifyJwtTokenInDto,
    handler: Annotated[
        VerifyJwtTokenHandler, Depends(verify_jwt_token_handler_dependency)
    ],
):
    return await handler.execute(body)
