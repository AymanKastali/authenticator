from fastapi import Depends, Request

from adapters.dto.request_dto.refresh_jwt_token import RefreshJwtTokenDto
from delivery.bootstrap.containers.auth import jwt_auth_container
from delivery.web.fastapi.api.v1.handlers.auth_handlers.jwt_refresh_token_handler import (
    JwtRefreshTokenHandler,
)


async def jwt_refresh_token_endpoint(
    _: Request,
    request_body: RefreshJwtTokenDto,
    handler: JwtRefreshTokenHandler = Depends(
        lambda: jwt_auth_container.jwt_refresh_token_handler
    ),
):
    return await handler.execute(request_body)
