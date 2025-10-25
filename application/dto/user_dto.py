from dataclasses import dataclass


@dataclass(frozen=True)
class UserDto:
    uid: str
    email: str
    active: bool
    verified: bool
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class PublicUserDto:
    uid: str
    email: str
    active: bool
    verified: bool = False


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
