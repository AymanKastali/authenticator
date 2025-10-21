from enum import StrEnum, auto


class Role(StrEnum):
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
