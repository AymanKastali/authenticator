from fastapi import Depends

from application.ports.services.logger import LoggerPort
from application.use_cases.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserUseCase,
)
from application.use_cases.auth.jwt.logout import LogoutUserUseCase
from application.use_cases.auth.jwt.refresh_tokens import RefreshTokensUseCase
from application.use_cases.auth.jwt.verify_access_token import (
    VerifyAccessTokenUseCase,
)
from application.use_cases.auth.login.jwt_login import JwtLoginUserUseCase
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
    jwt_login_user_uc_dependency,
    jwt_logout_user_uc_dependency,
    jwt_refresh_tokens_uc_dependency,
    jwt_verify_access_token_uc_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.infrastructure.logger import (
    get_console_json_logger,
)


def jwt_login_controller_dependency(
    login_user: JwtLoginUserUseCase = Depends(jwt_login_user_uc_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> JwtLoginController:
    return JwtLoginController(login_user, logger)


def jwt_logout_controller_dependency(
    logout_user: LogoutUserUseCase = Depends(jwt_logout_user_uc_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> JwtLogoutController:
    return JwtLogoutController(logout_user, logger)


def jwt_refresh_tokens_controller_dependency(
    refresh_tokens: RefreshTokensUseCase = Depends(
        jwt_refresh_tokens_uc_dependency
    ),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> RefreshJwtTokenController:
    return RefreshJwtTokenController(refresh_tokens, logger)


def jwt_verify_access_token_controller_dependency(
    verify_access_token: VerifyAccessTokenUseCase = Depends(
        jwt_verify_access_token_uc_dependency
    ),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> VerifyJwtTokenController:
    return VerifyJwtTokenController(verify_access_token, logger)


def jwt_get_authenticated_user_controller_dependency(
    use_case: GetAuthenticatedUserUseCase = Depends(
        get_authenticated_user_uc_dependency
    ),
) -> GetAuthenticatedUserController:
    return GetAuthenticatedUserController(use_case)
