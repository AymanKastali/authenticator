from enum import StrEnum


class RouteTag(StrEnum):
    AUTH = "Auth"
    USERS = "Users"

    @classmethod
    def values(cls) -> list[str]:
        return [member.value for member in cls]
