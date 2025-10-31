# domain/value_objects/jwt_payload_vo.py
from dataclasses import dataclass, field
from datetime import datetime

from domain.utils.time import make_aware, utc_now
from domain.value_objects.email import Email
from domain.value_objects.identifiers import UUIDId
from domain.value_objects.jwt_token_type import JwtTokenType
from domain.value_objects.role import Role


@dataclass(frozen=True, kw_only=True)
class JwtPayloadVo:
    """Value Object representing the claims inside a JWT."""

    sub: UUIDId
    typ: JwtTokenType
    exp: datetime
    jti: UUIDId = field(default_factory=UUIDId.new)
    iat: datetime = field(default_factory=utc_now)
    nbf: datetime = field(default_factory=utc_now)
    iss: str | None = None
    aud: str | None = None
    roles: list[Role] = field(default_factory=list)
    email: Email | None = None
    username: str | None = None

    # --- domain invariants ---
    def __post_init__(self):
        object.__setattr__(self, "iat", make_aware(self.iat))
        object.__setattr__(self, "nbf", make_aware(self.nbf))
        object.__setattr__(self, "exp", make_aware(self.exp))

        if self.exp <= self.iat:
            raise ValueError("exp must be after iat")
        if self.nbf > self.exp:
            raise ValueError("nbf must not be after exp")
        if self.iat > utc_now():
            raise ValueError("iat cannot be in the future")

    # --- domain behavior ---
    def is_expired(self) -> bool:
        return utc_now() >= self.exp

    def to_primitives(self) -> dict:
        """Return primitive representation for serialization (infra use)."""
        return {
            "sub": str(self.sub),
            "typ": self.typ.value,
            "exp": int(self.exp.timestamp()),
            "jti": str(self.jti),
            "iat": int(self.iat.timestamp()),
            "nbf": int(self.nbf.timestamp()),
            "iss": self.iss,
            "aud": self.aud,
            "roles": [r.value for r in self.roles],
            "email": str(self.email) if self.email else None,
            "username": self.username,
        }

    # --- factory ---
    @classmethod
    def create(
        cls,
        *,
        sub: UUIDId,
        typ: JwtTokenType,
        exp: datetime,
        roles: list[Role] | None = None,
        email: Email | None = None,
        username: str | None = None,
        iss: str | None = "auth.myapp.com",
        aud: str | None = "api.myapp.com",
        nbf: datetime | None = None,
    ) -> "JwtPayloadVo":
        """Factory method to create a valid payload VO."""
        return cls(
            sub=sub,
            typ=typ,
            exp=exp,
            roles=roles or [],
            email=email,
            username=username,
            iss=iss,
            aud=aud,
            nbf=nbf or utc_now(),
        )
