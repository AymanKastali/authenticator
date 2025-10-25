from dataclasses import dataclass
from datetime import datetime

from application.dto.jwt_dto import JwtTokenPayloadDto
from domain.entities.jwt_token_payload import JwtTokenPayload
from domain.utils.date_time_utils import utc_now
from domain.value_objects.email import Email
from domain.value_objects.identifiers import UUIDId
from domain.value_objects.jwt_token_type import JwtTokenType
from domain.value_objects.role import Role


@dataclass
class JwtTokenPayloadMapper:
    @staticmethod
    def to_dto_from_entity(token: JwtTokenPayload) -> JwtTokenPayloadDto:
        return JwtTokenPayloadDto(
            sub=token.sub.to_string(),
            typ=token.typ.name,
            exp=token.exp.timestamp(),
            jti=token.jti.to_string(),
            iat=token.iat.timestamp(),
            iss=token.iss if token.iss else None,
            aud=token.aud if token.aud else None,
            nbf=token.nbf.timestamp(),
            roles=[role.name for role in token.roles] if token.roles else [],
            email=token.email.to_string() if token.email else None,
            username=token.username if token.username else None,
        )

    @staticmethod
    def to_dict_from_dto(token: JwtTokenPayloadDto) -> dict:
        """Convert the DTO to a dict suitable for JSON encoding or JWT payload."""
        data = {
            "sub": token.sub,
            "type": token.typ,
            "jti": token.jti,
            "iat": token.iat,
            "exp": token.exp,
            "nbf": token.nbf,
            "roles": token.roles or [],
        }

        if token.iss is not None:
            data["iss"] = token.iss
        if token.aud is not None:
            data["aud"] = token.aud
        if token.email is not None:
            data["email"] = token.email
        if token.username is not None:
            data["username"] = token.username

        return data

    @staticmethod
    def to_dto_from_dict(data: dict) -> JwtTokenPayloadDto:
        """
        Convert a dictionary (decoded JWT payload) to JwtTokenPayloadDto.
        """
        return JwtTokenPayloadDto(
            sub=data["sub"],
            typ=data["type"],
            exp=data["exp"],
            jti=data.get("jti", ""),
            iat=data.get("iat", 0),
            iss=data.get("iss"),
            aud=data.get("aud"),
            nbf=data.get("nbf", 0),
            roles=data.get("roles", []),
            email=data.get("email"),
            username=data.get("username"),
        )

    @staticmethod
    def to_entity_from_dict(data: dict) -> JwtTokenPayload:
        """
        Convert a dict (decoded JWT) back to a JwtTokenPayload entity.
        """
        return JwtTokenPayload(
            sub=UUIDId.from_string(data["sub"]),
            typ=JwtTokenType[data["type"]],
            exp=datetime.fromtimestamp(data["exp"]),
            jti=UUIDId.from_string(data.get("jti", UUIDId.new().to_string())),
            iat=datetime.fromtimestamp(data.get("iat", utc_now().timestamp())),
            iss=data.get("iss"),
            aud=data.get("aud"),
            nbf=datetime.fromtimestamp(data.get("nbf", utc_now().timestamp())),
            roles=[Role[name] for name in data.get("roles", [])],
            email=Email.from_string(data["email"])
            if data.get("email")
            else None,
            username=data.get("username"),
        )

    # @staticmethod
    # def from_entity(entity: JwtTokenPayload) -> "JwtTokenPayloadMapper":
    #     return JwtTokenPayloadMapper(
    #         sub=entity.sub.to_string(),
    #         typ=entity.typ.value,
    #         jti=entity.jti.to_string(),
    #         iat=entity.iat.timestamp(),
    #         exp=entity.exp.timestamp(),
    #         nbf=entity.nbf.timestamp(),
    #         iss=entity.iss,
    #         aud=entity.aud,
    #         roles=[r.value for r in entity.roles],
    #         email=entity.email.to_string() if entity.email else None,
    #         username=entity.username,
    #     )

    # def to_entity(self) -> JwtTokenPayload:
    #     return JwtTokenPayload(
    #         sub=UUIDId.from_string(self.sub),
    #         typ=JwtTokenType(self.typ),
    #         jti=UUIDId.from_string(self.jti),
    #         iat=datetime.fromtimestamp(self.iat),
    #         exp=datetime.fromtimestamp(self.exp),
    #         nbf=datetime.fromtimestamp(self.nbf),
    #         iss=self.iss,
    #         aud=self.aud,
    #         roles=[Role(r) for r in (self.roles or [])],
    #         email=Email(self.email) if self.email else None,
    #         username=self.username,
    #     )

    # def to_dict(self) -> dict:
    #     """Convert the DTO to a dict suitable for JSON encoding or JWT payload."""
    #     data = {
    #         "sub": self.sub,
    #         "type": self.typ,
    #         "jti": self.jti,
    #         "iat": self.iat,
    #         "exp": self.exp,
    #         "nbf": self.nbf,
    #         "roles": self.roles or [],
    #     }

    #     if self.iss is not None:
    #         data["iss"] = self.iss
    #     if self.aud is not None:
    #         data["aud"] = self.aud
    #     if self.email is not None:
    #         data["email"] = self.email
    #     if self.username is not None:
    #         data["username"] = self.username

    #     return data

    # @classmethod
    # def from_dict(cls, data: dict) -> "JwtTokenPayloadMapper":
    #     """Construct a DTO from a dict (e.g., decoded JWT)."""
    #     return cls(
    #         sub=data["sub"],
    #         typ=data["type"],
    #         jti=data["jti"],
    #         iat=float(data["iat"]),
    #         exp=float(data["exp"]),
    #         nbf=float(data["nbf"]),
    #         iss=data.get("iss"),
    #         aud=data.get("aud"),
    #         roles=data.get("roles", []),
    #         email=data.get("email"),
    #         username=data.get("username"),
    #     )

    # @classmethod
    # def to_dict_from_entity(cls, entity: JwtTokenPayload) -> dict:
    #     """Convert a domain entity directly to a dict for JWT signing."""
    #     dto = cls.from_entity(entity)
    #     return dto.to_dict()

    # @classmethod
    # def dict_to_entity(cls, data: dict) -> JwtTokenPayload:
    #     """Convert a dict (e.g., decoded JWT) directly to a domain entity."""
    #     dto = cls.from_dict(data)
    #     return dto.to_entity()
