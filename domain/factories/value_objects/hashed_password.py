from domain.interfaces.password_hasher import PasswordHasherInterface
from domain.interfaces.policy import PolicyInterface
from domain.value_objects.hashed_password import HashedPasswordVo


class HashedPasswordVoFactory:
    """
    Responsible for creating HashedPasswordVo correctly.
    Enforces policies and hashes the password.
    """

    @classmethod
    def from_plain(
        cls,
        plain: str,
        hasher: PasswordHasherInterface,
        policies: list[PolicyInterface],
    ) -> HashedPasswordVo:
        for policy in policies:
            policy.enforce(plain)

        hashed: str = hasher.hash(plain)
        return HashedPasswordVo(_value=hashed)
