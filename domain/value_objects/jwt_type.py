from enum import StrEnum, auto


class JwtTypeVo(StrEnum):
    ACCESS = auto()
    REFRESH = auto()

    @classmethod
    def from_string(cls, value: str) -> "JwtTypeVo":
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"Invalid JwtTypeVo value: {value}")

    @classmethod
    def values(cls) -> list[str]:
        return [member.value for member in cls]
