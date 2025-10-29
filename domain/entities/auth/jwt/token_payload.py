from dataclasses import dataclass, field
from datetime import datetime

from domain.utils.time import make_aware, utc_now
from domain.value_objects.email import Email
from domain.value_objects.identifiers import UUIDId
from domain.value_objects.jwt_token_type import JwtTokenType
from domain.value_objects.role import Role


@dataclass(frozen=True, kw_only=True)
class JwtTokenPayloadEntity:
    sub: UUIDId
    typ: JwtTokenType
    exp: datetime

    jti: UUIDId = field(default_factory=UUIDId.new)
    iat: datetime = field(default_factory=utc_now)
    iss: str | None = None
    aud: str | None = None
    nbf: datetime = field(default_factory=utc_now)
    roles: list[Role] = field(default_factory=list)
    email: Email | None = None
    username: str | None = None

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

    @classmethod
    def create(
        cls,
        sub: UUIDId,
        typ: JwtTokenType,
        exp: datetime,
        roles: list[Role] | None = None,
        email: Email | None = None,
        username: str | None = None,
        iss: str | None = "auth.myapp.com",
        aud: str | None = "api.myapp.com",
        nbf: datetime | None = None,
    ) -> "JwtTokenPayloadEntity":
        """Factory method to create a new payload."""
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
