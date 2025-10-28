from pydantic import BaseModel, ConfigDict


class JwtResponseResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class JwtTokenPayloadOutDto(BaseModel):
    user_id: str
    token_type: str
    expires_at: float
    email: str | None = None
    username: str | None = None
    roles: list[str] = []
