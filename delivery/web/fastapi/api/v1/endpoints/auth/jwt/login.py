from fastapi import Depends, Request

from adapters.dto.requests.auth.registration.login import LoginUserInDto
from delivery.web.fastapi.api.v1.dependencies.jwt import (
    jwt_login_handler_dependency,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.login import JwtLoginHandler


async def jwt_login_endpoint(
    _: Request,
    body: LoginUserInDto,
    handler: JwtLoginHandler = Depends(jwt_login_handler_dependency),
):
    return await handler.execute(body)
