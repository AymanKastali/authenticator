from fastapi import Depends, Request

from adapters.dto.request_dto.jwt_request_dto import RefreshJwtTokenInDto
from delivery.bootstrap.containers.auth import jwt_auth_container
from delivery.web.fastapi.api.v1.handlers.auth.jwt.refresh_token import (
    RefreshJwtTokenHandler,
)


async def refresh_jwt_token_endpoint(
    _: Request,
    body: RefreshJwtTokenInDto,
    handler: RefreshJwtTokenHandler = Depends(
        lambda: jwt_auth_container.jwt_refresh_token_handler
    ),
):
    return await handler.execute(body)
