from fastapi import Depends

from domain.config.config_models import JwtDomainConfig
from domain.ports.repositories.jwt import JwtRedisRepositoryPort
from domain.ports.services.jwt import JwtServicePort
from domain.services.jwt import JwtDomainService
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


def jwt_domain_service_dependency(
    jwt_service: JwtServicePort = Depends(jwt_service_dependency),
    jwt_redis_repo: JwtRedisRepositoryPort = Depends(jwt_redis_dependency),
    config: JwtDomainConfig = Depends(jwt_domain_config_dependency),
) -> JwtDomainService:
    policies = jwt_policies()
    return JwtDomainService(
        jwt_service=jwt_service,
        jwt_redis_repo=jwt_redis_repo,
        config=config,
        policies=policies,
    )
