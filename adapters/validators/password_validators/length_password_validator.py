from application.abstracts.abstract_password_validator import (
    AbstractPasswordValidator,
)


class LengthPasswordValidator(AbstractPasswordValidator):
    """Validates min and max password length."""

    def __init__(self, min_length: int = 8, max_length: int = 128):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, password: str) -> None:
        if not isinstance(password, str):
            self._raise("Password must be a string.")
        if len(password) < self.min_length:
            self._raise(
                f"Password too short. Minimum {self.min_length} characters."
            )
        if len(password) > self.max_length:
            self._raise(
                f"Password too long. Maximum {self.max_length} characters."
            )
