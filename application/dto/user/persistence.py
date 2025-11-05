from dataclasses import dataclass, field


@dataclass(frozen=True)
class PersistenceUserDto:
    uid: str
    email: str
    status: str
    created_at: str
    updated_at: str
    deleted_at: str | None = None
    hashed_password: str | None = None
    roles: list[str] = field(default_factory=list)
