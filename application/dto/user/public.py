from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PublicUserDto:
    uid: str
    email: str
    status: str
