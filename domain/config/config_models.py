from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordConfig:
    min_length: int
    max_length: int


@dataclass(frozen=True)
class LoginConfig:
    max_login_attempts: int
    enable_two_factor_auth: bool
    password_expiration_days: int
