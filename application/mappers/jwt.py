from dataclasses import dataclass
from datetime import datetime, timezone

from application.dto.auth.jwt.payload import JwtPayloadDto
from application.dto.auth.jwt.token import JwtDto
from domain.entities.auth.jwt.token import JwtEntity
from domain.value_objects.email import Email
from domain.value_objects.identifiers import UUIDId
from domain.value_objects.jwt_payload import JwtPayloadVo
from domain.value_objects.jwt_token_type import JwtTokenType
from domain.value_objects.role import Role


@dataclass
class JwtMapper:
    @staticmethod
    def to_payload_dto_from_vo(vo: JwtPayloadVo) -> JwtPayloadDto:
        return JwtPayloadDto(
            sub=vo.sub.to_string(),
            typ=vo.typ.name,
            exp=vo.exp.timestamp(),
            jti=vo.jti.to_string(),
            iat=vo.iat.timestamp(),
            iss=vo.iss if vo.iss else None,
            aud=vo.aud if vo.aud else None,
            nbf=vo.nbf.timestamp(),
            roles=[role.name for role in vo.roles] if vo.roles else [],
            email=vo.email.to_string() if vo.email else None,
            username=vo.username if vo.username else None,
        )

    @staticmethod
    def to_payload_vo_from_dto(dto: JwtPayloadDto) -> JwtPayloadVo:
        return JwtPayloadVo(
            sub=UUIDId.from_string(dto.sub),
            typ=JwtTokenType[dto.typ],
            exp=datetime.fromtimestamp(dto.exp, tz=timezone.utc),
            jti=UUIDId.from_string(dto.jti),
            iat=datetime.fromtimestamp(dto.iat, tz=timezone.utc),
            nbf=datetime.fromtimestamp(dto.nbf, tz=timezone.utc),
            roles=[Role[r] for r in dto.roles],
            email=Email(dto.email) if dto.email else None,
            username=dto.username,
            iss=dto.iss,
            aud=dto.aud,
        )

    # ---------------- Full JWT ----------------
    @staticmethod
    def to_entity_from_jwt_dto(dto: JwtDto) -> "JwtEntity":
        """Map application JwtDto → domain JwtEntity."""
        payload_vo = JwtMapper.to_payload_vo_from_dto(dto.payload)
        return JwtEntity.create_signed(
            payload=payload_vo, signature=dto.signature, header=dto.headers
        )

    @staticmethod
    def to_jwt_dto_from_entity(entity: JwtEntity) -> JwtDto:
        """Map domain JwtEntity → application JwtDto."""
        payload_dto = JwtMapper.to_payload_dto_from_vo(entity.payload)
        return JwtDto(
            payload=payload_dto,
            headers=entity.header,
            signature=entity.signature,
        )

    @staticmethod
    def to_payload_dto_from_dict(decoded: dict) -> JwtPayloadDto:
        """
        Convert a decoded JWT dictionary into a JwtPayloadDto,
        enforcing domain VO invariants.
        """
        vo = JwtMapper.to_payload_vo_from_dto(JwtPayloadDto(**decoded))
        return JwtMapper.to_payload_dto_from_vo(vo)
