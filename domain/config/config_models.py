from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True, kw_only=True)
class LoginConfig:
    max_login_attempts: int
    enable_two_factor_auth: bool
    password_expiration_days: int


@dataclass(frozen=True, slots=True, kw_only=True)
class JwtDomainConfig:
    access_token_exp_seconds: int
    refresh_token_exp_seconds: int
    algorithm: str
    issuer: str | None = field(default=None)
    audience: str | None = field(default=None)
