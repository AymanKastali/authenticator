from dataclasses import dataclass


@dataclass(frozen=True)
class PersistenceUserDto:
    uid: str
    email: str
    hashed_password: str | None
    active: bool
    verified: bool
    created_at: str
    updated_at: str
    deleted_at: str | None
    roles: list[str]
