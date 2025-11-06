from datetime import datetime, timezone
from functools import lru_cache
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis

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
from infrastructure.config.jwt import JwtConfig
from infrastructure.exceptions.adapters_errors import (
    JWTExpiredError,
    JWTInvalidError,
)
from infrastructure.gateways.authentication.jwt_service import JwtService
from infrastructure.gateways.persistence.cache.redis.asynchronous.blacklist_adapter import (
    AsyncJwtBlacklistRedisAdapter,
)
from presentation.db.in_memory.repositories import get_in_memory_user_repository
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
from presentation.web.fastapi.api.v1.dependencies.logger import (
    get_console_json_logger,
)
from presentation.web.fastapi.schemas.response.auth.jwt.authenticated_user import (
    AuthenticatedUserResponseSchema,
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

        if await blacklist_cache.is_jwt_blacklisted(payload_dto.jti):
            raise JWTInvalidError("Token revoked/blacklisted")

        return payload_dto

    except (JWTExpiredError, JWTInvalidError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e


async def fetch_authenticated_user(
    user_id: UUID, user_controller: GetAuthenticatedUserController
) -> AuthenticatedUserResponseSchema:
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
        jwt_authenticated_user_controller_dependency
    ),
    blacklist_cache: AsyncJwtBlacklistRedisPort = Depends(
        get_jwt_blacklist_adapter
    ),
) -> AuthenticatedUserResponseSchema:
    """
    Validate JWT token, check expiration/blacklist, and return the authenticated user.
    """
    payload_dto = await validate_jwt_token(token, jwt_service, blacklist_cache)
    user = await fetch_authenticated_user(
        UUID(payload_dto.sub), user_controller
    )
    return user


def get_current_authenticated_active_user(
    current_user: AuthenticatedUserResponseSchema = Depends(
        get_current_authenticated_user
    ),
) -> AuthenticatedUserResponseSchema:
    """
    Ensure the authenticated user is active.
    Raises 403 if user is inactive.
    """
    if not current_user.status.lower() == "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user
