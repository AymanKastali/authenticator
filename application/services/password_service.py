from application.abstracts.abstract_password_validator import (
    AbstractPasswordValidator,
)
from domain.value_objects.hashed_password import HashedPassword


class PasswordService:
    def __init__(self, validators: list[AbstractPasswordValidator]):
        if not validators:
            raise ValueError(
                "At least one password validator must be provided."
            )
        self._validators = validators

    def _validate(self, password: str) -> None:
        for validator in self._validators:
            validator.validate(password)

    def create_hashed_password(self, password: str) -> HashedPassword:
        self._validate(password)
        return HashedPassword.from_plain(password)
