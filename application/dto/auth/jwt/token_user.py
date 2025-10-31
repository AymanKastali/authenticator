from dataclasses import dataclass, field


@dataclass(frozen=True)
class TokenUserDto:
    uid: str
    email: str
    active: bool
    verified: bool
    created_at: str
    updated_at: str
    deleted_at: str | None = field(default=None)
    roles: list[str] = field(default_factory=list)
