from pydantic import BaseModel, Field


class VerifyJwtTokenRequestSchema(BaseModel):
    token: str
    subject: str | None = Field(
        default=None, description="user sub to validate against"
    )
