from datetime import datetime, timezone
from functools import lru_cache
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from adapters.config.jwt import JwtConfig
from adapters.controllers.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserController,
)
from adapters.controllers.auth.jwt.login import LoginJwtController
from adapters.controllers.auth.jwt.logout import LogoutJwtController
from adapters.controllers.auth.jwt.refresh_token import (
    RefreshJwtTokenController,
)
from adapters.controllers.auth.jwt.verify_token import VerifyJwtTokenController
from adapters.dto.responses.auth.jwt.authenticated_user import (
    AuthenticatedUserOutDto,
)
from adapters.exceptions.adapters_errors import JWTExpiredError, JWTInvalidError
from adapters.gateways.authentication.jwt_service import JwtService
from application.dto.auth.jwt.payload import JwtPayloadDto
from application.dto.auth.jwt.token import JwtDto
from application.ports.repositories.user import UserRepositoryPort
from application.ports.services.jwt import JwtServicePort
from application.ports.services.logger import LoggerPort
from application.services.auth.authentication import AuthService
from application.services.auth.jwt.auth import JwtAuthService
from application.services.auth.jwt.facade import JwtAuthFacade
from application.use_cases.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserUseCase,
)
from delivery.db.in_memory.repositories import get_in_memory_user_repository
from delivery.web.fastapi.api.v1.dependencies.logger import (
    get_console_json_logger,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.login import JwtLoginHandler
from delivery.web.fastapi.api.v1.handlers.auth.jwt.logout import (
    JwtLogoutHandler,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.refresh_token import (
    RefreshJwtTokenHandler,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.verify_token import (
    VerifyJwtTokenHandler,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/jwt/login")


# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------
@lru_cache
def jwt_config_dependency() -> JwtConfig:
    """Provide cached JwtConfig (singleton)."""
    return JwtConfig()


# -----------------------------------------------------------------------------
# SERVICES
# -----------------------------------------------------------------------------
def jwt_service_dependency(
    jwt_cfg: JwtConfig = Depends(jwt_config_dependency),
) -> JwtServicePort:
    """Provide JwtService implementation."""
    return JwtService(jwt_cfg)


def auth_service_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
) -> AuthService:
    """Provide AuthService."""
    return AuthService(user_repo)


def jwt_auth_service_dependency(
    jwt_service: JwtServicePort = Depends(jwt_service_dependency),
) -> JwtAuthService:
    """Provide JwtAuthService."""
    return JwtAuthService(jwt_service)


def jwt_auth_facade_service_dependency(
    auth_service: AuthService = Depends(auth_service_dependency),
    jwt_auth_service: JwtAuthService = Depends(jwt_auth_service_dependency),
) -> JwtAuthFacade:
    """Provide JwtAuthFacade service."""
    return JwtAuthFacade(
        auth_service=auth_service,
        jwt_auth_service=jwt_auth_service,
        # blacklist_cache=get_jwt_blacklist_adapter()  # Optional future addition
    )


# -----------------------------------------------------------------------------
# USE CASES
# -----------------------------------------------------------------------------
def get_authenticated_user_uc_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
) -> GetAuthenticatedUserUseCase:
    """Provide use case for retrieving the authenticated user."""
    return GetAuthenticatedUserUseCase(user_repo)


# -----------------------------------------------------------------------------
# CONTROLLERS
# -----------------------------------------------------------------------------
def login_jwt_controller_dependency(
    jwt_facade_service: JwtAuthFacade = Depends(
        jwt_auth_facade_service_dependency
    ),
) -> LoginJwtController:
    return LoginJwtController(jwt_facade_service)


def refresh_jwt_token_controller_dependency(
    jwt_facade_service: JwtAuthFacade = Depends(
        jwt_auth_facade_service_dependency
    ),
) -> RefreshJwtTokenController:
    return RefreshJwtTokenController(jwt_facade_service)


def verify_jwt_token_controller_dependency(
    jwt_facade_service: JwtAuthFacade = Depends(
        jwt_auth_facade_service_dependency
    ),
) -> VerifyJwtTokenController:
    return VerifyJwtTokenController(jwt_facade_service)


def get_authenticated_user_controller_dependency(
    use_case: GetAuthenticatedUserUseCase = Depends(
        get_authenticated_user_uc_dependency
    ),
) -> GetAuthenticatedUserController:
    return GetAuthenticatedUserController(use_case)


def logout_jwt_controller_dependency(
    jwt_facade_service: JwtAuthFacade = Depends(
        jwt_auth_facade_service_dependency
    ),
) -> LogoutJwtController:
    return LogoutJwtController(jwt_facade_service)


# -----------------------------------------------------------------------------
# HANDLERS
# -----------------------------------------------------------------------------
def jwt_login_handler_dependency(
    controller: LoginJwtController = Depends(login_jwt_controller_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> JwtLoginHandler:
    return JwtLoginHandler(controller, logger)


def jwt_refresh_token_handler_dependency(
    controller: RefreshJwtTokenController = Depends(
        refresh_jwt_token_controller_dependency
    ),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> RefreshJwtTokenHandler:
    return RefreshJwtTokenHandler(controller, logger)


def verify_jwt_token_handler_dependency(
    controller: VerifyJwtTokenController = Depends(
        verify_jwt_token_controller_dependency
    ),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> VerifyJwtTokenHandler:
    return VerifyJwtTokenHandler(controller, logger)


def jwt_logout_handler_dependency(
    controller: LogoutJwtController = Depends(logout_jwt_controller_dependency),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> JwtLogoutHandler:
    return JwtLogoutHandler(controller, logger)


# -----------------------------------------------------------------------------
# VALIDATION
# -----------------------------------------------------------------------------
def get_current_authenticated_user(
    token: str = Depends(oauth2_scheme),
    jwt_service: JwtServicePort = Depends(jwt_service_dependency),
    user_controller: GetAuthenticatedUserController = Depends(
        get_authenticated_user_controller_dependency
    ),
) -> AuthenticatedUserOutDto:
    """
    Validate JWT token, check expiration, and return the authenticated user.
    """
    try:
        token_dto: JwtDto = jwt_service.verify(token)
        payload_dto: JwtPayloadDto = token_dto.payload

        if datetime.now(timezone.utc).timestamp() >= payload_dto.exp:
            raise JWTExpiredError("Token expired")

        # Optional: check blacklist
        # if jwt_service.is_blacklisted(payload_dto.jti):
        #     raise JWTInvalidError("Token revoked/blacklisted")

    except (JWTExpiredError, JWTInvalidError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e

    user = user_controller.execute(UUID(payload_dto.sub))
    return user


def get_current_authenticated_active_user(
    current_user: AuthenticatedUserOutDto = Depends(
        get_current_authenticated_user
    ),
):
    """
    Ensure the authenticated user is active.
    """
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user
