from fastapi import Depends

from adapters.controllers.login_jwt_controller import JwtLoginController
from adapters.controllers.login_session_controller import SessionLoginController
from adapters.controllers.register_user_controller import RegisterUserController
from delivery.web.fastapi.api.v1.dependencies.auth_dependencies.controller_dependencies import (
    get_jwt_login_controller,
    get_register_user_controller,
    get_session_login_controller,
)
from delivery.web.fastapi.api.v1.handlers.login_jwt_handler import (
    JwtLoginHandler,
)
from delivery.web.fastapi.api.v1.handlers.login_session_handler import (
    SessionLoginHandler,
)
from delivery.web.fastapi.api.v1.handlers.register_user_handler import (
    RegisterUserHandler,
)


def get_jwt_login_handler(
    controller: JwtLoginController = Depends(get_jwt_login_controller),
) -> JwtLoginHandler:
    return JwtLoginHandler(controller)


def get_session_login_handler(
    controller: SessionLoginController = Depends(get_session_login_controller),
) -> SessionLoginHandler:
    return SessionLoginHandler(controller)


def get_register_user_handler(
    controller: RegisterUserController = Depends(get_register_user_controller),
) -> RegisterUserHandler:
    return RegisterUserHandler(controller)
