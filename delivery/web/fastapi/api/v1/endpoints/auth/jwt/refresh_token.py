from fastapi import Depends, Request

from adapters.dto.requests.auth.jwt.refresh_token import RefreshJwtTokenInDto
from delivery.web.fastapi.api.v1.dependencies.jwt import (
    jwt_refresh_token_handler_dependency,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.refresh_token import (
    RefreshJwtTokenHandler,
)


async def refresh_jwt_token_endpoint(
    _: Request,
    body: RefreshJwtTokenInDto,
    handler: RefreshJwtTokenHandler = Depends(
        jwt_refresh_token_handler_dependency
    ),
):
    return await handler.execute(body)
