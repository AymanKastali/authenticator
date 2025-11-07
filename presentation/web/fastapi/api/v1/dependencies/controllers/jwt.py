from fastapi import Depends

from application.ports.services.logger import LoggerPort
from application.services.auth.jwt.auth import JwtAuthService
from application.use_cases.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserUseCase,
)
from presentation.web.fastapi.api.v1.controllers.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserController,
)
from presentation.web.fastapi.api.v1.controllers.auth.jwt.login import (
    JwtLoginController,
)
from presentation.web.fastapi.api.v1.controllers.auth.jwt.logout import (
    JwtLogoutController,
)
from presentation.web.fastapi.api.v1.controllers.auth.jwt.refresh_token import (
    RefreshJwtTokenController,
)
from presentation.web.fastapi.api.v1.controllers.auth.jwt.verify_token import (
    VerifyJwtTokenController,
)
from presentation.web.fastapi.api.v1.dependencies.application.jwt import (
    get_authenticated_user_uc_dependency,
    jwt_auth_service_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.infrastructure.logger import (
    get_console_json_logger,
)


def jwt_login_controller_dependency(
    service: JwtAuthService = Depends(jwt_auth_service_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> JwtLoginController:
    return JwtLoginController(service, logger)


def jwt_refresh_token_controller_dependency(
    service: JwtAuthService = Depends(jwt_auth_service_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> RefreshJwtTokenController:
    return RefreshJwtTokenController(service, logger)


def jwt_verify_token_controller_dependency(
    service: JwtAuthService = Depends(jwt_auth_service_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> VerifyJwtTokenController:
    return VerifyJwtTokenController(service, logger)


def jwt_logout_controller_dependency(
    service: JwtAuthService = Depends(jwt_auth_service_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> JwtLogoutController:
    return JwtLogoutController(service, logger)


def jwt_authenticated_user_controller_dependency(
    use_case: GetAuthenticatedUserUseCase = Depends(
        get_authenticated_user_uc_dependency
    ),
) -> GetAuthenticatedUserController:
    return GetAuthenticatedUserController(use_case)
