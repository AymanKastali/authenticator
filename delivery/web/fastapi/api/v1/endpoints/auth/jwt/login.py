from fastapi import Depends, Request

from adapters.dto.request_dto.login_user_model import LoginUserModel
from delivery.bootstrap.containers.auth import jwt_auth_container
from delivery.web.fastapi.api.v1.handlers.auth_handlers.jwt_login_handler import (
    JwtLoginHandler,
)


async def jwt_login_endpoint(
    _: Request,
    request_body: LoginUserModel,
    handler: JwtLoginHandler = Depends(
        lambda: jwt_auth_container.jwt_login_handler
    ),
):
    return await handler.execute(request_body)
