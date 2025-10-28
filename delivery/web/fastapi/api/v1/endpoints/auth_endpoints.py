from fastapi import Depends, Request, Response

from adapters.dto.request_dto.login_user_model import LoginUserModel
from adapters.dto.request_dto.refresh_jwt_token import RefreshJwtTokenDto
from delivery.bootstrap.containers import (
    feature_auth_container as auth_controller,
)
from delivery.web.fastapi.api.v1.handlers.auth_handlers.jwt_login_handler import (
    JwtLoginHandler,
)
from delivery.web.fastapi.api.v1.handlers.auth_handlers.jwt_refresh_token_handler import (
    JwtRefreshTokenHandler,
)
from delivery.web.fastapi.api.v1.handlers.auth_handlers.login_session_handler import (
    SessionLoginHandler,
)
from delivery.web.fastapi.api.v1.handlers.auth_handlers.register_user_handler import (
    RegisterUserHandler,
)


async def register_user_endpoint(
    _: Request,
    request_body: LoginUserModel,
    handler: RegisterUserHandler = Depends(
        lambda: auth_controller.register_user_handler
    ),
):
    return await handler.execute(request_body)


async def jwt_login_endpoint(
    _: Request,
    request_body: LoginUserModel,
    handler: JwtLoginHandler = Depends(
        lambda: auth_controller.jwt_login_handler
    ),
):
    return await handler.execute(request_body)


async def jwt_refresh_token_endpoint(
    _: Request,
    request_body: RefreshJwtTokenDto,
    handler: JwtRefreshTokenHandler = Depends(
        lambda: auth_controller.jwt_refresh_token_handler
    ),
):
    return await handler.execute(request_body)


async def session_login_endpoint(
    _: Request,
    request_body: LoginUserModel,
    response: Response,
    handler: SessionLoginHandler = Depends(
        lambda: auth_controller.session_login_handler
    ),
):
    return await handler.execute(request_body, response)
