from fastapi import Depends, Request
from typing_extensions import Annotated

from adapters.dto.requests.auth.registration.login import LoginUserInDto
from delivery.web.fastapi.api.v1.dependencies.jwt import (
    jwt_login_handler_dependency,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.login import JwtLoginHandler


async def jwt_login_endpoint(
    _request: Request,
    body: LoginUserInDto,
    handler: Annotated[JwtLoginHandler, Depends(jwt_login_handler_dependency)],
):
    return await handler.execute(body)
