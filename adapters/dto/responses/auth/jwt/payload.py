from pydantic import BaseModel


class JwtTokenPayloadOutDto(BaseModel):
    user_id: str
    token_type: str
    expires_at: float
    email: str | None = None
    username: str | None = None
    roles: list[str] = []
