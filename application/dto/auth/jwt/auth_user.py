from dataclasses import dataclass, field


@dataclass(frozen=True)
class AuthUserDto:
    uid: str
    email: str
    status: str
    created_at: str
    updated_at: str
    roles: list[str] = field(default_factory=list)
