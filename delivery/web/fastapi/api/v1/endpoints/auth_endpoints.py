from fastapi import Depends, Request

from adapters.request_models.login_user_model import LoginUserModel
from delivery.web.fastapi.api.v1.dependencies.auth_dependencies.handler_dependencies import (
    get_login_user_handler,
)
from delivery.web.fastapi.api.v1.handlers.login_user_handler import (
    LoginUserHandler,
)


async def login_user_endpoint(
    _: Request,
    request_body: LoginUserModel,
    handler: LoginUserHandler = Depends(get_login_user_handler),
):
    return await handler.handle(request_body)
