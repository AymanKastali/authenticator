from dataclasses import dataclass

from adapters.config.jwt_config import JwtConfig


@dataclass(frozen=True, kw_only=True, slots=True)
class AdaptersConfig:
    """
    Immutable configuration for the domain layer.
    Composed of specialized configs for different concerns.
    """

    jwt: JwtConfig

    def __post_init__(self):
        self._validate_jwt_config()

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
