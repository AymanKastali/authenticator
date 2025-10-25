from dataclasses import dataclass

from domain.config.config_models import LoginConfig


@dataclass(frozen=True, kw_only=True, slots=True)
class DomainConfig:
    """
    Immutable configuration for the domain layer.
    Composed of specialized configs for different concerns.
    """

    login: LoginConfig

    def __post_init__(self):
        self._validate_login_config()

    def _validate_login_config(self) -> None:
        if self.login.max_login_attempts < 1:
            raise ValueError("login.max_login_attempts must be at least 1")
        if self.login.password_expiration_days < 1:
            raise ValueError(
                "login.password_expiration_days must be at least 1"
            )
