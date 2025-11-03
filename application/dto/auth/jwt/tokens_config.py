from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class TokensConfigDto:
    access_token_exp: int
    refresh_token_exp: int
    issuer: str | None = None
    audience: str | None = None
