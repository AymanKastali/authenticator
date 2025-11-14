from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True, kw_only=True)
class TokenUserDto:
    uid: str
    email: str
    status: str
    created_at: str
    updated_at: str
    deleted_at: str | None = field(default=None)
    roles: list[str] = field(default_factory=list)
