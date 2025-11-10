from dataclasses import dataclass

from application.dto.auth.jwt.header import JwtHeaderDto
from application.dto.auth.jwt.payload import JwtPayloadDto


@dataclass(frozen=True, kw_only=True)
class JwtDto:
    """DTO representing the full JWT (header + payload + signature)."""

    payload: JwtPayloadDto
    headers: JwtHeaderDto
    signature: str
