from enum import StrEnum, auto


class UserStatusVo(StrEnum):
    ACTIVE = auto()
    INACTIVE = auto()
    PENDING_VERIFICATION = auto()
    VERIFIED = auto()

    @classmethod
    def keys(cls) -> list["UserStatusVo"]:
        return list(cls)

    @classmethod
    def values(cls) -> list[str]:
        return [member.value for member in cls]

    @classmethod
    def from_string(cls, value: str) -> "UserStatusVo":
        """Convert a string to a UserStatusVo member, accepting lowercase input."""
        for member in cls:
            if member.value.upper() == value.upper():
                return member
        raise ValueError(
            f"Invalid UserStatusVo value: '{value}'. Allowed values: {cls.values()}"
        )
