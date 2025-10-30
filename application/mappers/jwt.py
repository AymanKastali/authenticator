from dataclasses import dataclass
from datetime import datetime

from application.dto.auth.jwt.token import JwtPayloadDto
from domain.entities.auth.jwt.token_payload import JwtTokenPayloadEntity
from domain.utils.time import utc_now
from domain.value_objects.email import Email
from domain.value_objects.identifiers import UUIDId
from domain.value_objects.jwt_token_type import JwtTokenType
from domain.value_objects.role import Role


@dataclass
class JwtPayloadMapper:
    @staticmethod
    def to_dto_from_entity(token: JwtTokenPayloadEntity) -> JwtPayloadDto:
        return JwtPayloadDto(
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
    def to_dict_from_dto(token: JwtPayloadDto) -> dict:
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
    def to_dto_from_dict(data: dict) -> JwtPayloadDto:
        """
        Convert a dictionary (decoded JWT payload) to JwtPayloadDto.
        """
        return JwtPayloadDto(
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
    def to_entity_from_dict(data: dict) -> JwtTokenPayloadEntity:
        """
        Convert a dict (decoded JWT) back to a JwtTokenPayloadEntity entity.
        """
        return JwtTokenPayloadEntity(
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
