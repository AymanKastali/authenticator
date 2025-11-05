from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class JwtTokensDto:
    access_token: str
    refresh_token: str
