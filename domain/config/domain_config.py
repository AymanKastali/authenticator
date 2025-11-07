from dataclasses import dataclass

from domain.config.config_models import JwtConfig, PasswordConfig


@dataclass(frozen=True, kw_only=True, slots=True)
class DomainConfig:
    """
    Immutable configuration for the domain layer.
    Composed of specialized configs for different concerns.
    """

    password_config: PasswordConfig
    jwt_config: JwtConfig
