from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordConfig:
    min_length: int
    max_length: int


@dataclass(frozen=True)
class JwtConfig:
    access_token_expiration_minutes: int
    refresh_token_expiration_days: int
    secret_key: str
    algorithm: str
    issuer: str
    audience: str
    leeway_seconds: int


@dataclass(frozen=True)
class LoginConfig:
    max_login_attempts: int
    enable_two_factor_auth: bool
    password_expiration_days: int
