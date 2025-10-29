from dataclasses import dataclass

from pwdlib import PasswordHash

from domain.interfaces.password_policy import PasswordPolicy

password_hash = PasswordHash.recommended()


@dataclass(frozen=True)
class HashedPassword:
    value: str

    @classmethod
    def from_plain(
        cls, password: str, policies: list[PasswordPolicy]
    ) -> "HashedPassword":
        for policy in policies:
            policy.enforce(password)
        hashed = password_hash.hash(password)
        return cls(value=hashed)

    def verify(self, password: str) -> bool:
        return password_hash.verify(password, self.value)
