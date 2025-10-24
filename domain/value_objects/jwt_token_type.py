from enum import StrEnum, auto


class JwtTokenType(StrEnum):
    ACCESS = auto()
    REFRESH = auto()

    @classmethod
    def values(cls) -> list[str]:
        return [member.value for member in cls]
