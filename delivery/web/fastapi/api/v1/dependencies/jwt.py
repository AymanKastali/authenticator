from datetime import datetime, timezone
from functools import lru_cache
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis

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
from adapters.gateways.persistence.cache.redis.asynchronous.blacklist_adapter import (
    AsyncJwtBlacklistRedisAdapter,
)
from application.dto.auth.jwt.payload import JwtPayloadDto
from application.dto.auth.jwt.token import JwtDto
from application.dto.auth.jwt.tokens_config import TokensConfigDto
from application.ports.cache.redis.jwt_blacklist import (
    AsyncJwtBlacklistRedisPort,
)
from application.ports.repositories.user import UserRepositoryPort
from application.ports.services.jwt import JwtServicePort
from application.ports.services.logger import LoggerPort
from application.services.auth.authentication import AuthService
from application.services.auth.jwt.auth import JwtAuthService
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
# CACHE
# -----------------------------------------------------------------------------
async def get_jwt_blacklist_adapter(
    request: Request,
) -> AsyncJwtBlacklistRedisPort:
    """Return a singleton JWT blacklist adapter."""
    redis_conn: Redis | None = getattr(request.app.state, "redis", None)
    return AsyncJwtBlacklistRedisAdapter(redis_conn)


# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------
@lru_cache
def jwt_config_dependency() -> JwtConfig:
    """Provide cached JwtConfig (singleton)."""
    return JwtConfig()


def tokens_config_dto_dependency(
    jwt_config: JwtConfig = Depends(jwt_config_dependency),
) -> TokensConfigDto:
    """Map adapter config to application DTO."""
    return TokensConfigDto(
        access_token_exp=jwt_config.access_token_exp,
        refresh_token_exp=jwt_config.refresh_token_exp,
        issuer=jwt_config.issuer,
        audience=jwt_config.audience,
    )


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


async def jwt_auth_service_dependency(
    auth_service: AuthService = Depends(auth_service_dependency),
    jwt_service: JwtServicePort = Depends(jwt_service_dependency),
    tokens_config: TokensConfigDto = Depends(tokens_config_dto_dependency),
    blacklist_cache: AsyncJwtBlacklistRedisPort = Depends(
        get_jwt_blacklist_adapter
    ),
) -> JwtAuthService:
    """Provide JwtAuthService."""
    return JwtAuthService(
        auth_service=auth_service,
        jwt_service=jwt_service,
        tokens_config=tokens_config,
        blacklist_cache=blacklist_cache,
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
    jwt_facade_service: JwtAuthService = Depends(jwt_auth_service_dependency),
) -> LoginJwtController:
    return LoginJwtController(jwt_facade_service)


def refresh_jwt_token_controller_dependency(
    jwt_facade_service: JwtAuthService = Depends(jwt_auth_service_dependency),
) -> RefreshJwtTokenController:
    return RefreshJwtTokenController(jwt_facade_service)


def verify_jwt_token_controller_dependency(
    jwt_facade_service: JwtAuthService = Depends(jwt_auth_service_dependency),
) -> VerifyJwtTokenController:
    return VerifyJwtTokenController(jwt_facade_service)


def get_authenticated_user_controller_dependency(
    use_case: GetAuthenticatedUserUseCase = Depends(
        get_authenticated_user_uc_dependency
    ),
) -> GetAuthenticatedUserController:
    return GetAuthenticatedUserController(use_case)


def logout_jwt_controller_dependency(
    jwt_facade_service: JwtAuthService = Depends(jwt_auth_service_dependency),
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
# HELPERS
# -----------------------------------------------------------------------------
async def validate_jwt_token(
    token: str,
    jwt_service: JwtServicePort,
    blacklist_cache: AsyncJwtBlacklistRedisPort,
) -> JwtPayloadDto:
    """
    Verify the JWT token, check expiration, and blacklist status.
    Returns the payload if valid.
    """
    try:
        token_dto: JwtDto = jwt_service.verify(token)
        payload_dto: JwtPayloadDto = token_dto.payload

        now_ts = datetime.now(timezone.utc).timestamp()
        if now_ts >= payload_dto.exp:
            raise JWTExpiredError("Token expired")

        print(
            "xxxxxxxxx",
            await blacklist_cache.is_jwt_blacklisted(payload_dto.jti),
        )

        if await blacklist_cache.is_jwt_blacklisted(payload_dto.jti):
            raise JWTInvalidError("Token revoked/blacklisted")

        return payload_dto

    except (JWTExpiredError, JWTInvalidError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e


async def fetch_authenticated_user(
    user_id: UUID, user_controller: GetAuthenticatedUserController
) -> AuthenticatedUserOutDto:
    """
    Fetch the authenticated user object by user ID.
    """
    return await user_controller.execute(user_id)


# -----------------------------------------------------------------------------
# VALIDATION
# -----------------------------------------------------------------------------
async def get_current_authenticated_user(
    token: str = Depends(oauth2_scheme),
    jwt_service: JwtServicePort = Depends(jwt_service_dependency),
    user_controller: GetAuthenticatedUserController = Depends(
        get_authenticated_user_controller_dependency
    ),
    blacklist_cache: AsyncJwtBlacklistRedisPort = Depends(
        get_jwt_blacklist_adapter
    ),
) -> AuthenticatedUserOutDto:
    """
    Validate JWT token, check expiration/blacklist, and return the authenticated user.
    """
    payload_dto = await validate_jwt_token(token, jwt_service, blacklist_cache)
    user = await fetch_authenticated_user(
        UUID(payload_dto.sub), user_controller
    )
    return user


def get_current_authenticated_active_user(
    current_user: AuthenticatedUserOutDto = Depends(
        get_current_authenticated_user
    ),
) -> AuthenticatedUserOutDto:
    """
    Ensure the authenticated user is active.
    Raises 403 if user is inactive.
    """
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user
