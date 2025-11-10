from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class JwtHeaderDto:
    algorithm: str
    type: str
    key_id: str | None = None
