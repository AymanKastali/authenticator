from enum import StrEnum, auto


class RoleVo(StrEnum):
    # Super admin roles
    SUPER_ADMIN = auto()

    # Administration roles
    ADMIN = auto()
    MODERATOR = auto()

    # Standard user roles
    USER = auto()
    GUEST = auto()

    # Content roles
    EDITOR = auto()
    AUTHOR = auto()
    CONTRIBUTOR = auto()
    REVIEWER = auto()

    # System / service roles
    API_CLIENT = auto()
    SERVICE_ACCOUNT = auto()

    # Specialized roles (example for e-commerce)
    CUSTOMER = auto()
    VENDOR = auto()
    SUPPORT_AGENT = auto()

    # Additional example roles
    ANALYST = auto()
    FINANCE = auto()
    MARKETING = auto()

    @classmethod
    def values(cls) -> list[str]:
        return [member.value for member in cls]

    @classmethod
    def from_string(cls, value: str) -> "RoleVo":
        """Convert a string to a RoleVo member, accepting lowercase input."""
        for member in cls:
            if member.value.upper() == value.upper():
                return member
        raise ValueError(
            f"Invalid RoleVo value: '{value}'. Allowed values: {cls.values()}"
        )
