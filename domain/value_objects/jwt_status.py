from enum import StrEnum, auto
from typing import Self


class JwtStatusVo(StrEnum):
    ACTIVE = auto()
    REVOKED = auto()
    EXPIRED = auto()

    @classmethod
    def from_string(cls, value: str) -> Self:
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"Invalid {cls.__name__} value: {value}")

    @classmethod
    def values(cls) -> list[str]:
        return [member.value for member in cls]
