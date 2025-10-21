from dataclasses import dataclass

from pwdlib import PasswordHash

from domain.config.config_models import PasswordConfig
from domain.exceptions.domain_exceptions import PasswordError

password_hash = PasswordHash.recommended()


@dataclass(frozen=True)
class HashedPassword:
    value: str

    _cfg: PasswordConfig

    @classmethod
    def from_plain(cls, password: str, cfg: PasswordConfig) -> "HashedPassword":
        cls._validate_is_string(password)
        cls._validate_min_length(password, cfg)
        cls._validate_max_length(password, cfg)

        hashed = password_hash.hash(password)
        return HashedPassword(value=hashed, _cfg=cfg)

    @staticmethod
    def _validate_is_string(password: str) -> None:
        if not isinstance(password, str):
            raise PasswordError(
                field_name="password", message="Password must be a string."
            )

    @staticmethod
    def _validate_min_length(password: str, cfg: PasswordConfig) -> None:
        if len(password) < cfg.min_length:
            raise PasswordError(
                field_name="password",
                message=f"Password too short, minimum {cfg.min_length} characters.",
            )

    @staticmethod
    def _validate_max_length(password: str, cfg: PasswordConfig) -> None:
        if len(password) > cfg.max_length:
            raise PasswordError(
                field_name="password",
                message=f"Password too long, maximum {cfg.max_length} characters.",
            )

    def verify(self, password: str) -> bool:
        if not isinstance(password, str):
            return False
        return password_hash.verify(password, self.value)
