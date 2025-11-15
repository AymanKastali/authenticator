import secrets
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True, kw_only=True)
class SessionIdVo:
    value: str

    @classmethod
    def new(cls, length: int = 32) -> Self:
        token = secrets.token_urlsafe(length)
        return cls(value=token)

    @classmethod
    def from_string(cls, value: str) -> Self:
        return cls(value=value)

    def to_string(self) -> str:
        return self.value
