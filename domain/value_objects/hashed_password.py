from dataclasses import dataclass

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


@dataclass(frozen=True)
class HashedPassword:
    value: str

    @classmethod
    def from_plain(cls, password: str) -> "HashedPassword":
        # no config validation here
        hashed = password_hash.hash(password)
        return HashedPassword(value=hashed)

    def verify(self, password: str) -> bool:
        return password_hash.verify(password, self.value)
