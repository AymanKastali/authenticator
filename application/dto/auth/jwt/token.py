from dataclasses import dataclass

from application.dto.auth.jwt.payload import JwtPayloadDto


@dataclass(frozen=True, kw_only=True)
class JwtDto:
    """DTO representing the full JWT (header + payload + signature)."""

    payload: JwtPayloadDto
    headers: dict[str, str]
    signature: str
