from fastapi import Depends

from domain.config.config_models import JwtDomainConfig
from domain.interfaces.policy import PolicyInterface
from domain.ports.repositories.jwt import JwtRedisRepositoryPort
from domain.ports.services.jwt import JwtServicePort
from domain.services.auth.jwt.issue_jwt import IssueJwt
from domain.services.auth.jwt.revoke_jwt import RevokeJwt
from domain.services.auth.jwt.validate_jwt import ValidateJwt
from presentation.web.fastapi.api.v1.dependencies.domain.config import (
    jwt_domain_config_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.domain.policy import (
    jwt_policies,
)
from presentation.web.fastapi.api.v1.dependencies.infrastructure.jwt import (
    jwt_redis_dependency,
    jwt_service_dependency,
)


def jwt_issuance_dependency(
    jwt_service: JwtServicePort = Depends(jwt_service_dependency),
    config: JwtDomainConfig = Depends(jwt_domain_config_dependency),
    policies: list[PolicyInterface] = Depends(jwt_policies),
) -> IssueJwt:
    return IssueJwt(jwt_service=jwt_service, config=config, policies=policies)


def jwt_validation_dependency(
    jwt_service: JwtServicePort = Depends(jwt_service_dependency),
) -> ValidateJwt:
    return ValidateJwt(jwt_service=jwt_service)


def jwt_revocation_dependency(
    jwt_redis_repo: JwtRedisRepositoryPort = Depends(jwt_redis_dependency),
) -> RevokeJwt:
    return RevokeJwt(jwt_redis_repo=jwt_redis_repo)
