from fastapi import Depends, Request

from adapters.dto.requests.auth.jwt.logout import LogoutJwtInDto
from delivery.bootstrap.containers.auth import jwt_auth_container
from delivery.web.fastapi.api.v1.handlers.auth.jwt.logout import (
    JwtLogoutHandler,
)


async def jwt_logout_endpoint(
    _: Request,
    body: LogoutJwtInDto,
    handler: JwtLogoutHandler = Depends(
        lambda: jwt_auth_container.jwt_logout_handler
    ),
):
    return await handler.execute(body)
