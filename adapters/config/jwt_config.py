from dataclasses import dataclass


@dataclass(frozen=True)
class JwtConfig:
    secret_key: str
    algorithm: str
    issuer: str
    audience: str
    leeway: int
