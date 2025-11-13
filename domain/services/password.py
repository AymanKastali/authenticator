from domain.interfaces.policy import PolicyInterface
from domain.value_objects.hashed_password import HashedPasswordVo


class PasswordDomainService:
    def __init__(self, policies: list[PolicyInterface]):
        self._policies = policies

    def hash_password(self, plain_password: str) -> HashedPasswordVo:
        """Hash a password after validating all policies."""
        return HashedPasswordVo.create(plain_password, self._policies)

    def verify_password(
        self, plain_password: str, hashed_password: HashedPasswordVo
    ) -> bool:
        """Verify that a plain password matches a hashed one."""
        return hashed_password.verify(plain_password)
