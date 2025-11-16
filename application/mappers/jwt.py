from typing import Any

from domain.entities.jwt_token import JwtEntity
from domain.factories.value_objects.claims import JwtClaimsVoFactory
from domain.factories.value_objects.header import JwtHeaderVoFactory
from domain.factories.value_objects.header_algorithm import (
    JwtHeaderAlgorithmVoFactory,
)
from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.jwt_claims import JwtClaimsVo
from domain.value_objects.jwt_header import JwtHeaderVo
from domain.value_objects.jwt_status import JwtStatusVo


class JwtMapper:
    """Mapper for serializing and deserializing JWT entities and value objects."""

    # ----------------------- Claims -----------------------
    @classmethod
    def claims_to_dict(cls, claims: JwtClaimsVo) -> dict[str, Any]:
        """Serialize JwtClaimsVo to a dictionary suitable for JWT encoding."""

        def to_timestamp(vo: DateTimeVo) -> int:
            # Mapper knows how to convert DateTimeVo → primitive timestamp
            return int(vo.value.timestamp())

        return {
            "sub": claims.sub.value,
            "typ": claims.typ.value,
            "exp": to_timestamp(claims.exp),
            "jti": claims.jti.value,
            "iat": to_timestamp(claims.iat),
            "nbf": to_timestamp(claims.nbf),
            "iss": claims.iss,
            "aud": claims.aud,
            "email": claims.email.value if claims.email else None,
            "username": claims.username,
            "roles": [role.value for role in claims.roles],
            "extras": dict(claims.extras) if claims.extras else {},
        }

    @classmethod
    def dict_to_claims(cls, data: dict[str, Any]) -> JwtClaimsVo:
        """Reconstruct JwtClaimsVo from a dictionary (decoded JWT payload)."""
        return JwtClaimsVoFactory.from_dict(data)

    # ----------------------- Headers -----------------------
    @classmethod
    def headers_to_dict(cls, headers: JwtHeaderVo) -> dict[str, Any]:
        header_dict = {
            "alg": headers.alg.value,
            "typ": headers.typ,
        }
        if headers.kid is not None:
            header_dict["kid"] = str(headers.kid)  # ensure string
        return header_dict

    @classmethod
    def dict_to_headers(cls, data: dict[str, Any]) -> JwtHeaderVo:
        """Reconstruct JwtHeaderVo from a dictionary (decoded JWT headers)."""
        alg = JwtHeaderAlgorithmVoFactory.from_string(data["alg"])
        return JwtHeaderVoFactory.create(alg, kid=data.get("kid"))

    # ----------------------- Entity -----------------------
    @classmethod
    def entity_to_dict(cls, entity: JwtEntity) -> dict[str, dict[str, Any]]:
        """Serialize entire JwtEntity (claims + headers) for JWT encoding."""
        return {
            "claims": cls.claims_to_dict(entity.claims),
            "headers": cls.headers_to_dict(entity.headers),
        }

    @classmethod
    def dict_to_entity(
        cls, claims_data: dict[str, Any], headers_data: dict[str, Any]
    ) -> JwtEntity:
        """Reconstruct JwtEntity from decoded JWT data."""
        claims_vo = cls.dict_to_claims(claims_data)
        headers_vo = cls.dict_to_headers(headers_data)

        return JwtEntity(
            status=JwtStatusVo.ACTIVE,
            claims=claims_vo,
            headers=headers_vo,
        )
