from domain.interfaces.password_policy import PasswordPolicy
from domain.value_objects.hashed_password import HashedPassword


class PasswordService:
    def __init__(self, policies: list[PasswordPolicy]):
        self._policies = policies

    def create_hashed_password(self, password: str) -> HashedPassword:
        return HashedPassword.from_plain(password, self._policies)
