from fastapi import Depends, Request

from adapters.dto.requests.auth.registration.login import LoginUserInDto
from delivery.bootstrap.containers.auth import jwt_auth_container
from delivery.web.fastapi.api.v1.handlers.auth.jwt.login import JwtLoginHandler


async def jwt_login_endpoint(
    _: Request,
    body: LoginUserInDto,
    handler: JwtLoginHandler = Depends(
        lambda: jwt_auth_container.jwt_login_handler
    ),
):
    return await handler.execute(body)
