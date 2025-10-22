from fastapi import Depends, Request, Response

from adapters.presenters.request_models.login_user_model import LoginUserModel
from delivery.web.fastapi.api.v1.dependencies.auth_dependencies.handler_dependencies import (
    get_jwt_login_handler,
    get_register_user_handler,
    get_session_login_handler,
)
from delivery.web.fastapi.api.v1.handlers.auth_handlers.login_jwt_handler import (
    JwtLoginHandler,
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
    handler: RegisterUserHandler = Depends(get_register_user_handler),
):
    return await handler.execute(request_body)


async def jwt_login_endpoint(
    _: Request,
    request_body: LoginUserModel,
    handler: JwtLoginHandler = Depends(get_jwt_login_handler),
):
    return await handler.execute(request_body)


async def session_login_endpoint(
    _: Request,
    request_body: LoginUserModel,
    response: Response,
    handler: SessionLoginHandler = Depends(get_session_login_handler),
):
    return await handler.execute(request_body, response)
