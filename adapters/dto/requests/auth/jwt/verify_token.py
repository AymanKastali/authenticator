from pydantic import BaseModel, Field


class VerifyJwtTokenInDto(BaseModel):
    token: str
    subject: str | None = Field(
        default=None, description="user sub to validate against"
    )
