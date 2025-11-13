from dataclasses import dataclass

from application.dto.auth.jwt.claims import JwtClaimsDto
from application.dto.auth.jwt.header import JwtHeaderDto


@dataclass(frozen=True, kw_only=True)
class JwtDto:
    """DTO representing the full JWT (header + claims + signature)."""

    claims: JwtClaimsDto
    headers: JwtHeaderDto
    signature: str
