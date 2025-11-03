from typing import Annotated

from fastapi import Depends, Request

from adapters.dto.requests.auth.jwt.logout import LogoutJwtInDto
from adapters.dto.responses.auth.jwt.authenticated_user import (
    AuthenticatedUserOutDto,
)
from delivery.web.fastapi.api.v1.dependencies.jwt import (
    get_current_authenticated_user,
    jwt_logout_handler_dependency,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.logout import (
    JwtLogoutHandler,
)


async def jwt_logout_endpoint(
    _request: Request,
    body: LogoutJwtInDto,
    _authenticated_user: Annotated[
        AuthenticatedUserOutDto, Depends(get_current_authenticated_user)
    ],
    handler: Annotated[
        JwtLogoutHandler, Depends(jwt_logout_handler_dependency)
    ],
):
    return await handler.execute(body)
