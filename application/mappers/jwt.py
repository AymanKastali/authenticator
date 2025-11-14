from dataclasses import dataclass

from application.dto.auth.jwt.claims import JwtClaimsDto
from domain.value_objects.jwt_claims import JwtClaimsVo


@dataclass
class JwtMapper:
    @staticmethod
    def to_claims_dto_from_vo(vo: JwtClaimsVo) -> JwtClaimsDto:
        return JwtClaimsDto(
            sub=vo.sub.to_string(),
            typ=vo.typ.value,
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
