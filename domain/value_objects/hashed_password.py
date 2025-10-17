from dataclasses import dataclass
from hashlib import sha256


@dataclass(frozen=True)
class HashedPassword:
    value: str

    @staticmethod
    def from_plain(password: str) -> "HashedPassword":
        if len(password) < 8:
            raise ValueError("Password too short.")
        hashed = sha256(password.encode()).hexdigest()
        return HashedPassword(hashed)

    def verify(self, password: str) -> bool:
        return self.value == sha256(password.encode()).hexdigest()
