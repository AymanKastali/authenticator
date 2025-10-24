from dataclasses import dataclass

from domain.config.config_models import LoginConfig, PasswordConfig


@dataclass(frozen=True, kw_only=True, slots=True)
class DomainConfig:
    """
    Immutable configuration for the domain layer.
    Composed of specialized configs for different concerns.
    """

    password: PasswordConfig
    login: LoginConfig

    def __post_init__(self):
        self._validate_login_config()
        self._validate_password_config()

    def _validate_login_config(self) -> None:
        if self.login.max_login_attempts < 1:
            raise ValueError("login.max_login_attempts must be at least 1")
        if self.login.password_expiration_days < 1:
            raise ValueError(
                "login.password_expiration_days must be at least 1"
            )

    def _validate_password_config(self) -> None:
        if self.password.min_length < 1:
            raise ValueError("password.min_length must be at least 1")
        if self.password.max_length < self.password.min_length:
            raise ValueError(
                "password.max_length must be greater than or equal to password.min_length"
            )
