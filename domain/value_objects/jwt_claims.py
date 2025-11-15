from dataclasses import dataclass, field
from typing import Any, Mapping

from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.email import EmailVo
from domain.value_objects.jwt_type import JwtTypeVo
from domain.value_objects.role import RoleVo
from domain.value_objects.uuid_id import UUIDVo


@dataclass(frozen=True, slots=True, kw_only=True)
class JwtClaimsVo:
    """Represents JWT claims as a Value Object with strong validation and modern Python style."""

    sub: UUIDVo
    typ: JwtTypeVo
    exp: DateTimeVo
    jti: UUIDVo
    iat: DateTimeVo
    nbf: DateTimeVo
    iss: str | None = None
    aud: str | None = None
    email: EmailVo | None = None
    username: str | None = None
    roles: list[RoleVo] = field(default_factory=list)
    extras: Mapping[str, Any] = field(default_factory=dict)
