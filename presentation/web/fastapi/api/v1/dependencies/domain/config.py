from functools import lru_cache

from domain.config.config_models import JwtDomainConfig, PasswordDomainConfig
from infrastructure.config import jwt_config


@lru_cache
def password_config_dependency() -> PasswordDomainConfig:
    return PasswordDomainConfig()


@lru_cache
def jwt_domain_config_dependency() -> JwtDomainConfig:
    cfg = jwt_config()
    return JwtDomainConfig(
        access_token_exp_seconds=cfg.access_token_exp,
        refresh_token_exp_seconds=cfg.refresh_token_exp,
        issuer=cfg.issuer,
        audience=cfg.audience,
    )
