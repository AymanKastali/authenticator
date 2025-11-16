from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, kw_only=True)
class JwtClaimsDto:
    sub: str
    typ: str
    exp: float

    jti: str
    iat: float
    nbf: float
    iss: str | None = None
    aud: str | None = None
    roles: list[str] = field(default_factory=list)
    email: str | None = None
    username: str | None = None
    extras: dict[str, Any] = field(default_factory=dict)
    is_valid: bool = True
