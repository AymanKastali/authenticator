from dataclasses import dataclass

from pwdlib import PasswordHash

from domain.exceptions.domain_exceptions import PasswordError

password_hash = PasswordHash.recommended()


@dataclass(frozen=True)
class HashedPassword:
    value: str

    @classmethod
    def _validate_is_string(cls, password: str) -> None:
        if not isinstance(password, str):
            raise PasswordError(
                field_name="password", message="Password must be a string."
            )

    @classmethod
    def _validate_min_length(cls, password: str) -> None:
        if len(password) < 8:
            raise PasswordError(
                field_name="password",
                message=f"Password too short, minimum {8} characters.",
            )

    @classmethod
    def _validate_max_length(cls, password: str) -> None:
        if len(password) > 128:
            raise PasswordError(
                field_name="password",
                message=f"Password too long, maximum {128} characters.",
            )

    @classmethod
    def from_plain(cls, password: str) -> "HashedPassword":
        cls._validate_is_string(password)
        cls._validate_min_length(password)
        cls._validate_max_length(password)

        hashed = password_hash.hash(password)
        return HashedPassword(value=hashed)

    def verify(self, password: str) -> bool:
        if not isinstance(password, str):
            return False
        return password_hash.verify(password, self.value)
