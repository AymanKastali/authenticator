from dataclasses import dataclass, field

from domain.value_objects.jwt_header_algorithm import JwtHeaderAlgorithmVo

_HEADER_TYPE: str = "JWT"


@dataclass(frozen=True, slots=True, kw_only=True)
class JwtHeaderVo:
    alg: JwtHeaderAlgorithmVo
    typ: str = field(default=_HEADER_TYPE)
    kid: str | None = field(default=None)
