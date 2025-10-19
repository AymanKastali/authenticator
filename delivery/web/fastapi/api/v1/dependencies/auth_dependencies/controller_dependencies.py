from fastapi import Depends

from adapters.controllers.auth_controller import AuthController
from application.use_cases.login_user_use_case import LoginUserUseCase
from delivery.web.fastapi.api.v1.dependencies.auth_dependencies.usecase_dependencies import (
    get_login_user_use_case,
)


def get_login_user_controller(
    use_case: LoginUserUseCase = Depends(get_login_user_use_case),
) -> AuthController:
    return AuthController(use_case)
