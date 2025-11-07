from dataclasses import dataclass
from typing import Mapping

from application.dto.auth.jwt.payload import JwtPayloadDto


@dataclass(frozen=True, kw_only=True)
class JwtDto:
    """DTO representing the full JWT (header + payload + signature)."""

    payload: JwtPayloadDto
    headers: Mapping[str, str]
    signature: str
