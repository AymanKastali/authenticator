from dataclasses import dataclass

from application.dto.auth.jwt.header import JwtHeaderDto
from application.dto.auth.jwt.payload import JwtPayloadDto
from application.dto.auth.jwt.token import JwtDto
from domain.entities.auth.jwt.token import JwtEntity
from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.email import EmailVo
from domain.value_objects.identifiers import UUIDVo
from domain.value_objects.jwt_header import JwtHeaderVo
from domain.value_objects.jwt_header_algorithm import JwtHeaderAlgorithmVo
from domain.value_objects.jwt_payload import JwtPayloadVo
from domain.value_objects.jwt_type import JwtTypeVo
from domain.value_objects.role import RoleVo


@dataclass
class JwtMapper:
    @staticmethod
    def to_payload_dto_from_vo(vo: JwtPayloadVo) -> JwtPayloadDto:
        return JwtPayloadDto(
            sub=vo.sub.to_string(),
            typ=vo.typ.name,
            exp=vo.exp.to_timestamp(),
            jti=vo.jti.to_string(),
            iat=vo.iat.to_timestamp(),
            iss=vo.iss if vo.iss else None,
            aud=vo.aud if vo.aud else None,
            nbf=vo.nbf.to_timestamp(),
            roles=[role.value for role in vo.roles] if vo.roles else [],
            email=vo.email.to_string() if vo.email else None,
            username=vo.username if vo.username else None,
        )

    @staticmethod
    def to_header_dto_from_vo(vo: JwtHeaderVo) -> JwtHeaderDto:
        return JwtHeaderDto(algorithm=vo.alg, type=vo.typ, key_id=vo.kid)

    @staticmethod
    def to_payload_vo_from_dto(dto: JwtPayloadDto) -> JwtPayloadVo:
        return JwtPayloadVo(
            sub=UUIDVo.from_string(dto.sub),
            typ=JwtTypeVo[dto.typ],
            exp=DateTimeVo.from_timestamp(dto.exp),
            jti=UUIDVo.from_string(dto.jti),
            iat=DateTimeVo.from_timestamp(dto.iat),
            nbf=DateTimeVo.from_timestamp(dto.nbf),
            roles=[RoleVo[r] for r in dto.roles],
            email=EmailVo.from_string(dto.email) if dto.email else None,
            username=dto.username,
            iss=dto.iss,
            aud=dto.aud,
        )

    @staticmethod
    def to_header_vo_from_dto(dto: JwtHeaderDto) -> JwtHeaderVo:
        return JwtHeaderVo(
            alg=JwtHeaderAlgorithmVo.from_string(dto.algorithm),
            typ=dto.type,
            kid=dto.key_id,
        )

    @staticmethod
    def to_payload_vo_from_dict(decoded: dict) -> JwtPayloadVo:
        return JwtPayloadVo(
            sub=UUIDVo.from_string(decoded["sub"]),
            jti=UUIDVo.from_string(
                decoded.get("jti", UUIDVo.new().to_string())
            ),
            typ=JwtTypeVo.from_string(decoded["typ"]),
            exp=DateTimeVo.from_timestamp(decoded["exp"]),
            iat=DateTimeVo.from_timestamp(decoded["iat"]),
            nbf=DateTimeVo.from_timestamp(decoded.get("nbf", decoded["iat"])),
            roles=[RoleVo.from_string(r) for r in decoded.get("roles", [])],
            email=EmailVo.from_string(decoded["email"])
            if decoded.get("email")
            else None,
            username=decoded.get("username"),
            iss=decoded.get("iss"),
            aud=decoded.get("aud"),
        )

    # ---------------- Full JWT ----------------
    @staticmethod
    def to_entity_from_jwt_dto(dto: JwtDto) -> "JwtEntity":
        """Map application JwtDto → domain JwtEntity."""
        payload_vo = JwtMapper.to_payload_vo_from_dto(dto.payload)
        header_vo = JwtMapper.to_header_vo_from_dto(dto.headers)
        return JwtEntity.create_signed(
            payload=payload_vo, signature=dto.signature, headers=header_vo
        )

    @staticmethod
    def to_jwt_dto_from_entity(entity: JwtEntity) -> JwtDto:
        """Map domain JwtEntity → application JwtDto."""
        payload_dto = JwtMapper.to_payload_dto_from_vo(entity.payload)
        header_dto = JwtMapper.to_header_dto_from_vo(entity.headers)

        return JwtDto(
            payload=payload_dto, headers=header_dto, signature=entity.signature
        )

    @staticmethod
    def to_payload_dto_from_dict(decoded: dict) -> JwtPayloadDto:
        """
        Convert a decoded JWT dictionary into a JwtPayloadDto,
        enforcing domain VO invariants.
        """
        vo = JwtMapper.to_payload_vo_from_dto(JwtPayloadDto(**decoded))
        return JwtMapper.to_payload_dto_from_vo(vo)
