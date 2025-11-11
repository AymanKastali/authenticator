from dataclasses import dataclass

from pwdlib import PasswordHash

from domain.interfaces.policy import PolicyInterface

password_hash = PasswordHash.recommended()


@dataclass(frozen=True)
class HashedPasswordVo:
    value: str

    @classmethod
    def create(
        cls, password: str, policies: list[PolicyInterface]
    ) -> "HashedPasswordVo":
        for policy in policies:
            policy.enforce(password)
        hashed = password_hash.hash(password)
        return cls(value=hashed)

    @classmethod
    def from_string(cls, hashed_value: str) -> "HashedPasswordVo":
        """
        Create a HashedPasswordVo instance from an existing hashed string.
        """
        return cls(value=hashed_value)

    def verify(self, password: str) -> bool:
        if not password:
            return False
        return password_hash.verify(password, self.value)
