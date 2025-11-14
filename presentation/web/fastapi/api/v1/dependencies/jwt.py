from functools import lru_cache

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis

from application.ports.services.logger import LoggerPort
from application.use_cases.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserUseCase,
)
from application.use_cases.auth.jwt.logout import LogoutUserUseCase
from application.use_cases.auth.jwt.refresh_tokens import RefreshTokensUseCase
from application.use_cases.auth.jwt.validate_access_token import (
    ValidateAccessTokenUseCase,
)
from application.use_cases.auth.jwt.validate_refresh_token import (
    ValidateRefreshTokenUseCase,
)
from application.use_cases.auth.login.jwt_login import JwtLoginUserUseCase
from domain.config.config_models import JwtDomainConfig
from domain.exceptions.domain_errors import JwtRevokedError, UserNotFoundError
from domain.factories.jwt_factory import JwtFactory
from domain.interfaces.jwt_factory import JwtFactoryInterface
from domain.interfaces.policy import PolicyInterface
from domain.ports.repositories.jwt import JwtRedisRepositoryPort
from domain.ports.services.jwt import JwtServicePort
from domain.services.auth.authenticate.authenticate_user import AuthenticateUser
from domain.services.auth.jwt.assert_jwt_revocation import (
    AssertJwtRevocation,
)
from domain.services.auth.jwt.issue_jwt import IssueJwt
from domain.services.auth.jwt.revoke_jwt import RevokeJwt
from domain.services.auth.jwt.validate_jwt import ValidateJwt
from infrastructure.config import jwt_config
from infrastructure.config.jwt import JwtConfig
from infrastructure.exceptions.adapters_errors import (
    JwtExpiredError,
    JwtInvalidError,
)
from infrastructure.gateways.persistence.cache.redis.asynchronous.repository import (
    JwtRedisRepository,
)
from infrastructure.services.auth.jwt import JwtService
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
from presentation.web.fastapi.api.v1.dependencies.authentication import (
    authenticate_user_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.config import (
    jwt_domain_config_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.logger import (
    get_console_json_logger,
)
from presentation.web.fastapi.api.v1.dependencies.policy import jwt_policies
from presentation.web.fastapi.api.v1.dependencies.user import (
    query_user_dependency,
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
    return JwtFactory(config=config, policies=policies)


def jwt_issuance_dependency(
    service: JwtServicePort = Depends(jwt_service_dependency),
    factory: JwtFactoryInterface = Depends(jwt_factory_dependency),
) -> IssueJwt:
    return IssueJwt(service=service, factory=factory)


def jwt_validation_dependency(
    service: JwtServicePort = Depends(jwt_service_dependency),
    factory: JwtFactoryInterface = Depends(jwt_factory_dependency),
) -> ValidateJwt:
    return ValidateJwt(service=service, factory=factory)


def jwt_revoke_dependency(
    jwt_redis_repo: JwtRedisRepositoryPort = Depends(jwt_redis_dependency),
) -> RevokeJwt:
    return RevokeJwt(jwt_redis_repo=jwt_redis_repo)


def jwt_assert_revocation_dependency(
    jwt_redis_repo: JwtRedisRepositoryPort = Depends(jwt_redis_dependency),
) -> AssertJwtRevocation:
    return AssertJwtRevocation(jwt_redis_repo=jwt_redis_repo)


# Application
def get_authenticated_user_uc_dependency(
    validate_jwt: ValidateJwt = Depends(jwt_validation_dependency),
    assert_jwt_revocation: AssertJwtRevocation = Depends(
        jwt_assert_revocation_dependency
    ),
    query_user=Depends(query_user_dependency),
) -> GetAuthenticatedUserUseCase:
    return GetAuthenticatedUserUseCase(
        validate_jwt=validate_jwt,
        assert_jwt_revocation=assert_jwt_revocation,
        query_user=query_user,
    )


def jwt_login_user_uc_dependency(
    authenticate_user: AuthenticateUser = Depends(authenticate_user_dependency),
    issue_jwt: IssueJwt = Depends(jwt_issuance_dependency),
) -> JwtLoginUserUseCase:
    return JwtLoginUserUseCase(
        authenticate_user=authenticate_user, issue_jwt=issue_jwt
    )


def jwt_logout_user_uc_dependency(
    validate_jwt: ValidateJwt = Depends(jwt_validation_dependency),
    revoke_jwt: RevokeJwt = Depends(jwt_revoke_dependency),
) -> LogoutUserUseCase:
    return LogoutUserUseCase(validate_jwt=validate_jwt, revoke_jwt=revoke_jwt)


def jwt_refresh_tokens_uc_dependency(
    validate_jwt: ValidateJwt = Depends(jwt_validation_dependency),
    issue_jwt: IssueJwt = Depends(jwt_issuance_dependency),
    query_user=Depends(query_user_dependency),
) -> RefreshTokensUseCase:
    return RefreshTokensUseCase(
        query_user=query_user, issue_jwt=issue_jwt, validate_jwt=validate_jwt
    )


def jwt_validate_access_token_uc_dependency(
    validate_jwt: ValidateJwt = Depends(jwt_validation_dependency),
    assert_jwt_revocation: AssertJwtRevocation = Depends(
        jwt_assert_revocation_dependency
    ),
) -> ValidateAccessTokenUseCase:
    return ValidateAccessTokenUseCase(
        validate_jwt=validate_jwt, assert_jwt_revocation=assert_jwt_revocation
    )


def jwt_validate_refresh_token_uc_dependency(
    validate_jwt: ValidateJwt = Depends(jwt_validation_dependency),
) -> ValidateRefreshTokenUseCase:
    return ValidateRefreshTokenUseCase(validate_jwt=validate_jwt)


# Presentation
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


def jwt_validate_token_controller_dependency(
    validate_access_token: ValidateAccessTokenUseCase = Depends(
        jwt_validate_access_token_uc_dependency
    ),
    validate_refresh_token: ValidateRefreshTokenUseCase = Depends(
        jwt_validate_refresh_token_uc_dependency
    ),
    logger: LoggerPort = Depends(get_console_json_logger),
) -> ValidateJwtTokenController:
    return ValidateJwtTokenController(
        validate_access_token=validate_access_token,
        validate_refresh_token=validate_refresh_token,
        logger=logger,
    )


def jwt_get_authenticated_user_controller_dependency(
    use_case: GetAuthenticatedUserUseCase = Depends(
        get_authenticated_user_uc_dependency
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
