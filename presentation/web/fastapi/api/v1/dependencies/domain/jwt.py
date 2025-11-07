from functools import lru_cache

from fastapi import Depends

from domain.config.config_models import JwtConfig as JwtDomainConfig
from domain.ports.repositories.jwt import JwtRedisRepositoryPort
from domain.ports.services.jwt import JwtServicePort
from domain.services.jwt import JWTDomainService
from infrastructure.config import jwt_config
from presentation.web.fastapi.api.v1.dependencies.infrastructure.jwt import (
    jwt_redis_dependency,
    jwt_service_dependency,
)


@lru_cache
def jwt_config_dependency() -> JwtDomainConfig:
    """Provide cached JwtConfig (singleton)."""
    cfg = jwt_config()
    return JwtDomainConfig(
        access_token_exp_seconds=cfg.access_token_exp,
        refresh_token_exp_seconds=cfg.refresh_token_exp,
        issuer=cfg.issuer,
        audience=cfg.audience,
    )


def jwt_domain_service_dependency(
    jwt_service: JwtServicePort = Depends(jwt_service_dependency),
    jwt_redis_repo: JwtRedisRepositoryPort = Depends(jwt_redis_dependency),
    config: JwtDomainConfig = Depends(jwt_config_dependency),
) -> JWTDomainService:
    return JWTDomainService(
        jwt_service=jwt_service,
        jwt_redis_repo=jwt_redis_repo,
        config=config,
    )
