from functools import lru_cache

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis

from application.ports.repositories.jwt import JwtRedisRepositoryPort
from application.ports.services.jwt import JwtServicePort
from application.ports.services.logger import LoggerPort
from application.services.jwt.get_authenticated_user import (
    GetJwtAuthenticatedUserService,
)
from application.services.jwt.login import JwtLoginUserService
from application.services.jwt.logout import JwtLogoutUserService
from application.services.jwt.refresh_tokens import RefreshJwtTokensService
from application.services.jwt.validate_access_token import (
    ValidateJwtAccessTokenService,
)
from application.services.jwt.validate_refresh_token import (
    ValidateJwtRefreshTokenService,
)
from application.use_cases.auth.authenticate_user import AuthenticateUserUseCase
from application.use_cases.jwt.assert_jwt_revocation import (
    AssertJwtRevocationUseCase,
)
from application.use_cases.jwt.issue_jwt import IssueJwtUseCase
from application.use_cases.jwt.revoke_jwt import RevokeJwtUseCase
from application.use_cases.jwt.validate_jwt import ValidateJwtUseCase
from domain.config.config_models import JwtDomainConfig
from domain.exceptions.domain_errors import JwtRevokedError, UserNotFoundError
from domain.factories.entities.jwt import JwtEntityFactory
from domain.interfaces.jwt_factory import JwtFactoryInterface
from domain.interfaces.policy import PolicyInterface
from infrastructure.config import jwt_config
from infrastructure.config.jwt import JwtConfig
from infrastructure.exceptions.adapters_errors import (
    JwtExpiredError,
    JwtInvalidError,
)
from infrastructure.gateways.persistence.cache.redis.asynchronous.repository import (
    JwtRedisRepository,
)
from infrastructure.services.jwt import JwtService
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
from presentation.web.fastapi.api.v1.controllers.auth.jwt.validate_token import (
    ValidateJwtTokenController,
)
from presentation.web.fastapi.dependencies.authentication import (
    authenticate_user_uc_dependency,
)
from presentation.web.fastapi.dependencies.config import (
    jwt_domain_config_dependency,
)
from presentation.web.fastapi.dependencies.logger import (
    get_console_json_logger,
)
from presentation.web.fastapi.dependencies.policy import jwt_policies
from presentation.web.fastapi.dependencies.user import (
    user_repo_dependency,
)
from presentation.web.fastapi.schemas.response.auth.jwt.authenticated_user import (
    AuthenticatedUserResponseSchema,
)


# Infrastructure
@lru_cache
def jwt_config_dependency() -> JwtConfig:
    """Provide cached JwtDomainConfig (singleton)."""
    return jwt_config()


def jwt_service_dependency(
    config: JwtConfig = Depends(jwt_config_dependency),
) -> JwtServicePort:
    """Provide JwtService implementation."""
    return JwtService(config)


async def jwt_redis_dependency(request: Request) -> JwtRedisRepositoryPort:
    redis_conn: Redis | None = getattr(request.app.state, "redis", None)
    return JwtRedisRepository(redis_conn)


# Domain
def jwt_factory_dependency(
    config: JwtDomainConfig = Depends(jwt_domain_config_dependency),
    policies: list[PolicyInterface] = Depends(jwt_policies),
) -> JwtFactoryInterface:
    return JwtEntityFactory(config=config, policies=policies)


# Application
def jwt_validation_uc_dependency(
    service: JwtServicePort = Depends(jwt_service_dependency),
    factory: JwtFactoryInterface = Depends(jwt_factory_dependency),
) -> ValidateJwtUseCase:
    return ValidateJwtUseCase(service=service, factory=factory)


def jwt_revocation_uc_dependency(
    jwt_redis_repo: JwtRedisRepositoryPort = Depends(jwt_redis_dependency),
) -> RevokeJwtUseCase:
    return RevokeJwtUseCase(jwt_redis_repo=jwt_redis_repo)


def jwt_assert_revocation_uc_dependency(
    jwt_redis_repo: JwtRedisRepositoryPort = Depends(jwt_redis_dependency),
) -> AssertJwtRevocationUseCase:
    return AssertJwtRevocationUseCase(jwt_redis_repo=jwt_redis_repo)


def jwt_issuance_uc_dependency(
    service: JwtServicePort = Depends(jwt_service_dependency),
    factory: JwtFactoryInterface = Depends(jwt_factory_dependency),
) -> IssueJwtUseCase:
    return IssueJwtUseCase(service=service, factory=factory)


def get_jwt_authenticated_user_service_dependency(
    validate_jwt: ValidateJwtUseCase = Depends(jwt_validation_uc_dependency),
    assert_jwt_revocation: AssertJwtRevocationUseCase = Depends(
        jwt_assert_revocation_uc_dependency
    ),
    user_repo=Depends(user_repo_dependency),
) -> GetJwtAuthenticatedUserService:
    return GetJwtAuthenticatedUserService(
        validate_jwt=validate_jwt,
        assert_jwt_revocation=assert_jwt_revocation,
        user_repo=user_repo,
    )


def jwt_login_user_service_dependency(
    authenticate_user: AuthenticateUserUseCase = Depends(
        authenticate_user_uc_dependency
    ),
    issue_jwt: IssueJwtUseCase = Depends(jwt_issuance_uc_dependency),
) -> JwtLoginUserService:
    return JwtLoginUserService(
        authenticate_user=authenticate_user, issue_jwt=issue_jwt
    )


def jwt_logout_user_service_dependency(
    validate_jwt: ValidateJwtUseCase = Depends(jwt_validation_uc_dependency),
    revoke_jwt: RevokeJwtUseCase = Depends(jwt_revocation_uc_dependency),
) -> JwtLogoutUserService:
    return JwtLogoutUserService(
        validate_jwt=validate_jwt, revoke_jwt=revoke_jwt
    )


def jwt_refresh_tokens_service_dependency(
    validate_jwt: ValidateJwtUseCase = Depends(jwt_validation_uc_dependency),
    issue_jwt: IssueJwtUseCase = Depends(jwt_issuance_uc_dependency),
    user_repo=Depends(user_repo_dependency),
) -> RefreshJwtTokensService:
    return RefreshJwtTokensService(
        user_repo=user_repo, issue_jwt=issue_jwt, validate_jwt=validate_jwt
    )


def jwt_validate_access_token_service_dependency(
    validate_jwt: ValidateJwtUseCase = Depends(jwt_validation_uc_dependency),
    assert_jwt_revocation: AssertJwtRevocationUseCase = Depends(
        jwt_assert_revocation_uc_dependency
    ),
) -> ValidateJwtAccessTokenService:
    return ValidateJwtAccessTokenService(
        validate_jwt=validate_jwt, assert_jwt_revocation=assert_jwt_revocation
    )


def jwt_validate_refresh_token_service_dependency(
    validate_jwt: ValidateJwtUseCase = Depends(jwt_validation_uc_dependency),
) -> ValidateJwtRefreshTokenService:
    return ValidateJwtRefreshTokenService(validate_jwt=validate_jwt)


# Presentation
def jwt_login_controller_dependency(
    login_user: JwtLoginUserService = Depends(
        jwt_login_user_service_dependency
    ),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> JwtLoginController:
    return JwtLoginController(login_user, logger)


def jwt_logout_controller_dependency(
    logout_user: JwtLogoutUserService = Depends(
        jwt_logout_user_service_dependency
    ),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> JwtLogoutController:
    return JwtLogoutController(logout_user, logger)


def jwt_refresh_tokens_controller_dependency(
    refresh_tokens: RefreshJwtTokensService = Depends(
        jwt_refresh_tokens_service_dependency
    ),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> RefreshJwtTokenController:
    return RefreshJwtTokenController(refresh_tokens, logger)


def jwt_validate_token_controller_dependency(
    validate_access_token: ValidateJwtAccessTokenService = Depends(
        jwt_validate_access_token_service_dependency
    ),
    validate_refresh_token: ValidateJwtRefreshTokenService = Depends(
        jwt_validate_refresh_token_service_dependency
    ),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> ValidateJwtTokenController:
    return ValidateJwtTokenController(
        validate_access_token_service=validate_access_token,
        validate_refresh_token_service=validate_refresh_token,
        logger=logger,
    )


def jwt_get_authenticated_user_controller_dependency(
    use_case: GetJwtAuthenticatedUserService = Depends(
        get_jwt_authenticated_user_service_dependency
    ),
) -> GetAuthenticatedUserController:
    return GetAuthenticatedUserController(use_case)


# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/jwt/login")


async def get_current_authenticated_user(
    token: str = Depends(oauth2_scheme),
    controller: GetAuthenticatedUserController = Depends(
        jwt_get_authenticated_user_controller_dependency
    ),
) -> AuthenticatedUserResponseSchema:
    """
    Returns the currently authenticated user.
    Raises 401 if token is invalid.
    """
    try:
        return await controller.execute(token)
    except (
        UserNotFoundError,
        JwtExpiredError,
        JwtInvalidError,
        JwtRevokedError,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e


def get_current_authenticated_active_user(
    current_user: AuthenticatedUserResponseSchema = Depends(
        get_current_authenticated_user
    ),
) -> AuthenticatedUserResponseSchema:
    """
    Returns the currently authenticated user only if active.
    Raises 403 if user is inactive.
    """
    if current_user.status.lower() != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user
