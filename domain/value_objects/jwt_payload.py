from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Literal

from domain.value_objects.uids import UUIDId


@dataclass(frozen=True, kw_only=True)
class JwtPayload:
    # Standard claims
    sub: str  # user ID
    iat: datetime  # issued at
    exp: datetime  # expiration
    jti: str = field(default_factory=lambda: UUIDId.new().to_string())
    iss: str | None = None  # issuer
    aud: str | None = None  # audience
    nbf: datetime | None = None  # not before

    # Custom claims
    type: Literal["access", "refresh"]
    roles: list[str] | None = field(default_factory=list)
    email: str | None = None
    username: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)
