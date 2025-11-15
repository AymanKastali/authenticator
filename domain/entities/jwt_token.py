from dataclasses import dataclass
from typing import Self

from domain.value_objects.jwt_claims import JwtClaimsVo
from domain.value_objects.jwt_header import JwtHeaderVo
from domain.value_objects.jwt_status import JwtStatusVo
from domain.value_objects.uuid_id import UUIDVo


@dataclass(frozen=True, slots=True, kw_only=True)
class JwtEntity:
    """Entity representing a full JWT (header + claims + signature)."""

    status: JwtStatusVo
    claims: JwtClaimsVo
    headers: JwtHeaderVo
    # signing_key_id: str

    @property
    def uid(self) -> UUIDVo:
        return self.claims.jti

    @property
    def subject(self) -> UUIDVo:
        return self.claims.sub

    @property
    def is_active(self) -> bool:
        return self.status == JwtStatusVo.ACTIVE

    def is_expired(self) -> bool:
        return self.claims.exp.is_past()

    def _with_status(self, status: JwtStatusVo) -> Self:
        return type(self)(
            status=status, claims=self.claims, headers=self.headers
        )

    def revoke(self) -> Self:
        return self._with_status(JwtStatusVo.REVOKED)

    def activate(self) -> Self:
        return self._with_status(JwtStatusVo.ACTIVE)

    def expire(self) -> Self:
        return self._with_status(JwtStatusVo.EXPIRED)
