from pydantic import BaseModel, Field


class RefreshJwtTokenInDto(BaseModel):
    refresh_token: str


class VerifyJwtTokenInDto(BaseModel):
    token: str
    subject: str | None = Field(
        default=None, description="user sub to validate against"
    )
