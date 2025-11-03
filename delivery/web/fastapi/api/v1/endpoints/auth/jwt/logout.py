from fastapi import Depends, Request

from adapters.dto.requests.auth.jwt.logout import LogoutJwtInDto
from delivery.web.fastapi.api.v1.dependencies.jwt import (
    jwt_logout_handler_dependency,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.logout import (
    JwtLogoutHandler,
)


async def jwt_logout_endpoint(
    _: Request,
    body: LogoutJwtInDto,
    handler: JwtLogoutHandler = Depends(jwt_logout_handler_dependency),
):
    return await handler.execute(body)
