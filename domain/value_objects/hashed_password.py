from dataclasses import dataclass

from pwdlib import PasswordHash

from domain.interfaces.password_policy import PasswordPolicy

password_hash = PasswordHash.recommended()


@dataclass(frozen=True)
class HashedPasswordVo:
    value: str

    @classmethod
    def from_plain(
        cls, password: str, policies: list[PasswordPolicy]
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
        return password_hash.verify(password, self.value)
