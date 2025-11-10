from enum import StrEnum


class JwtHeaderAlgorithmVo(StrEnum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"
    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"
    ES256 = "ES256"
    ES384 = "ES384"
    ES512 = "ES512"
    PS256 = "PS256"
    PS384 = "PS384"
    PS512 = "PS512"
    NONE = "none"

    @classmethod
    def from_string(cls, value: str) -> "JwtHeaderAlgorithmVo":
        """
        Case-insensitive conversion from string to enum.
        Raises ValueError if invalid.
        """
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"Invalid {cls.__name__} value: {value}")

    @classmethod
    def values(cls) -> list[str]:
        """Return all valid string values."""
        return [member.value for member in cls]

    def __str__(self) -> str:
        """Return the string representation of the enum."""
        return self.value
