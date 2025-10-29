from dataclasses import dataclass


@dataclass(frozen=True)
class PublicUserDto:
    uid: str
    email: str
    active: bool
    verified: bool = False
