from dataclasses import dataclass, field


@dataclass(frozen=True)
class LoginConfig:
    max_login_attempts: int
    enable_two_factor_auth: bool
    password_expiration_days: int


@dataclass(frozen=True)
class PasswordConfig:
    min_length: int = field(default=8)
    max_length: int = field(default=128)
    require_upper: bool = field(default=True)
    require_lower: bool = field(default=True)
    require_digit: bool = field(default=True)
    require_special: bool = field(default=True)
