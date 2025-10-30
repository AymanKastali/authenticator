from dataclasses import dataclass, field


@dataclass(frozen=True, kw_only=True)
class JwtPayloadDto:
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
