from dataclasses import dataclass
from datetime import datetime

from domain.entities.jwt_token_payload import JwtTokenPayload
from domain.value_objects.email import Email
from domain.value_objects.jwt_token_type import JwtTokenType
from domain.value_objects.role import Role
from domain.value_objects.uids import UUIDId


@dataclass
class JwtTokenPayloadDTO:
    sub: str
    typ: str
    jti: str
    iat: float
    exp: float
    nbf: float
    iss: str | None = None
    aud: str | None = None
    roles: list[str] | None = None
    email: str | None = None
    username: str | None = None

    @classmethod
    def from_entity(cls, entity: JwtTokenPayload) -> "JwtTokenPayloadDTO":
        return cls(
            sub=entity.sub.to_string(),
            typ=entity.typ.value,
            jti=entity.jti.to_string(),
            iat=entity.iat.timestamp(),
            exp=entity.exp.timestamp(),
            nbf=entity.nbf.timestamp(),
            iss=entity.iss,
            aud=entity.aud,
            roles=[r.value for r in entity.roles],
            email=entity.email.to_string() if entity.email else None,
            username=entity.username,
        )

    def to_entity(self) -> JwtTokenPayload:
        return JwtTokenPayload(
            sub=UUIDId.from_string(self.sub),
            typ=JwtTokenType(self.typ),
            jti=UUIDId.from_string(self.jti),
            iat=datetime.fromtimestamp(self.iat),
            exp=datetime.fromtimestamp(self.exp),
            nbf=datetime.fromtimestamp(self.nbf),
            iss=self.iss,
            aud=self.aud,
            roles=[Role(r) for r in (self.roles or [])],
            email=Email(self.email) if self.email else None,
            username=self.username,
        )

    def to_dict(self) -> dict:
        """Convert the DTO to a dict suitable for JSON encoding or JWT payload."""
        data = {
            "sub": self.sub,
            "type": self.typ,
            "jti": self.jti,
            "iat": self.iat,
            "exp": self.exp,
            "nbf": self.nbf,
            "roles": self.roles or [],
        }

        if self.iss is not None:
            data["iss"] = self.iss
        if self.aud is not None:
            data["aud"] = self.aud
        if self.email is not None:
            data["email"] = self.email
        if self.username is not None:
            data["username"] = self.username

        return data

    @classmethod
    def from_dict(cls, data: dict) -> "JwtTokenPayloadDTO":
        """Construct a DTO from a dict (e.g., decoded JWT)."""
        return cls(
            sub=data["sub"],
            typ=data["type"],
            jti=data["jti"],
            iat=float(data["iat"]),
            exp=float(data["exp"]),
            nbf=float(data["nbf"]),
            iss=data.get("iss"),
            aud=data.get("aud"),
            roles=data.get("roles", []),
            email=data.get("email"),
            username=data.get("username"),
        )

    @classmethod
    def entity_to_dict(cls, entity: JwtTokenPayload) -> dict:
        """Convert a domain entity directly to a dict for JWT signing."""
        dto = cls.from_entity(entity)
        return dto.to_dict()

    @classmethod
    def dict_to_entity(cls, data: dict) -> JwtTokenPayload:
        """Convert a dict (e.g., decoded JWT) directly to a domain entity."""
        dto = cls.from_dict(data)
        return dto.to_entity()
