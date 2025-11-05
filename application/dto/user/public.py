from dataclasses import dataclass


@dataclass(frozen=True)
class PublicUserDto:
    uid: str
    email: str
    status: str
