from fastapi import Depends

from adapters.controllers.auth_controller import AuthController
from delivery.web.fastapi.api.v1.dependencies.auth_dependencies.controller_dependencies import (
    get_login_user_controller,
)
from delivery.web.fastapi.api.v1.handlers.login_user_handler import (
    LoginUserHandler,
)


def get_login_user_handler(
    controller: AuthController = Depends(get_login_user_controller),
) -> LoginUserHandler:
    return LoginUserHandler(controller)
