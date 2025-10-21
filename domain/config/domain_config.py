from dataclasses import dataclass

from domain.config.config_models import JwtConfig, LoginConfig, PasswordConfig


@dataclass(frozen=True, kw_only=True, slots=True)
class DomainConfig:
    """
    Immutable configuration for the domain layer.
    Composed of specialized configs for different concerns.
    """

    # Composed configs
    password: PasswordConfig
    jwt: JwtConfig
    login: LoginConfig

    def __post_init__(self):
        self._validate_login_config()
        self._validate_password_config()
        self._validate_jwt_config()

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

    def _validate_jwt_config(self) -> None:
        if self.jwt.access_token_expiration_minutes < 1:
            raise ValueError(
                "jwt.access_token_expiration_minutes must be at least 1"
            )

        if self.jwt.refresh_token_expiration_days < 1:
            raise ValueError(
                "jwt.refresh_token_expiration_days must be at least 1"
            )
        if not self.jwt.secret_key:
            raise ValueError("jwt.secret_key must not be empty")

        if (
            not self.jwt.algorithm
            or not isinstance(self.jwt.algorithm, str)
            or not self.jwt.algorithm.strip()
        ):
            raise ValueError("jwt.algorithm must be a non-empty string")

        if (
            not self.jwt.issuer
            or not isinstance(self.jwt.issuer, str)
            or not self.jwt.issuer.strip()
        ):
            raise ValueError("jwt.issuer must be a non-empty string")

        if (
            not self.jwt.audience
            or not isinstance(self.jwt.audience, str)
            or not self.jwt.audience.strip()
        ):
            raise ValueError("jwt.audience must be a non-empty string")

        if self.jwt.leeway_seconds < 0:
            raise ValueError("jwt.leeway_seconds must be 0 or greater")
