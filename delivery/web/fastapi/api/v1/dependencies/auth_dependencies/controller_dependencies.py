from fastapi import Depends

from adapters.controllers.login_jwt_controller import JwtLoginController
from adapters.controllers.login_session_controller import SessionLoginController
from adapters.controllers.register_user_controller import RegisterUserController
from application.use_cases.jwt_login import JwtLoginUseCase
from application.use_cases.register_user import RegisterUserUseCase
from application.use_cases.session_login import SessionLoginUseCase
from delivery.web.fastapi.api.v1.dependencies.auth_dependencies.use_case_dependencies import (
    get_jwt_login_uc,
    get_register_user_uc,
    get_session_login_uc,
)


def get_jwt_login_controller(
    use_case: JwtLoginUseCase = Depends(get_jwt_login_uc),
) -> JwtLoginController:
    return JwtLoginController(use_case)


def get_session_login_controller(
    use_case: SessionLoginUseCase = Depends(get_session_login_uc),
) -> SessionLoginController:
    return SessionLoginController(use_case)


def get_register_user_controller(
    use_case: RegisterUserUseCase = Depends(get_register_user_uc),
) -> RegisterUserController:
    return RegisterUserController(use_case)
