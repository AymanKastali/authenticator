from dataclasses import dataclass

from domain.factories.password_policy import PasswordPolicyBuilder
from domain.interfaces.password_policy import PasswordPolicyInterface
from domain.value_objects.hashed_password import HashedPasswordVo


@dataclass(frozen=True, slots=True)
class PasswordDomainService:
    policies: list[PasswordPolicyInterface]

    @classmethod
    def builder(cls) -> "PasswordPolicyBuilder":
        """Start a builder for custom policy configuration."""
        return PasswordPolicyBuilder()

    def hash_password(self, plain_password: str) -> HashedPasswordVo:
        """Hash a password after validating all policies."""
        return HashedPasswordVo.from_plain(plain_password, self.policies)

    def verify_password(
        self, plain_password: str, hashed_password: HashedPasswordVo
    ) -> bool:
        """Verify that a plain password matches a hashed one."""
        return hashed_password.verify(plain_password)
