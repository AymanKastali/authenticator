from dataclasses import dataclass


@dataclass(frozen=True)
class CurrentUserDto:
    uid: str
    email: str
    active: bool
    verified: bool
    created_at: str
    updated_at: str
