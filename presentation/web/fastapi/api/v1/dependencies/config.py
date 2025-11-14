from functools import lru_cache

from domain.config.config_models import JwtDomainConfig, PasswordDomainConfig
from infrastructure.config import jwt_config


# Config
@lru_cache
def password_domain_config_dependency() -> PasswordDomainConfig:
    return PasswordDomainConfig(
        min_length=8,
        max_length=128,
        require_upper=True,
        require_lower=True,
        require_digit=True,
        require_special=True,
    )


@lru_cache
def jwt_domain_config_dependency() -> JwtDomainConfig:
    config = jwt_config()
    return JwtDomainConfig(
        access_token_exp_seconds=config.access_token_exp,
        refresh_token_exp_seconds=config.refresh_token_exp,
        issuer=config.issuer,
        audience=config.audience,
        algorithm=config.algorithm,
    )
