from enum import StrEnum


class RouteTag(StrEnum):
    AUTH = "Auth"
    USERS = "Users"
    APP = "App"

    @classmethod
    def values(cls) -> list[str]:
        return [member.value for member in cls]
