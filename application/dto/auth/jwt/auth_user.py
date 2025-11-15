from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthUserDto:
    uid: str
    email: str
    status: str
    created_at: str
    roles: list[str] = field(default_factory=list)
