from typing import Literal

from pydantic import BaseModel, Field


class ValidateJwtTokenRequestSchema(BaseModel):
    token: str
    token_type: Literal["access", "refresh"]
    subject: str | None = Field(
        default=None, description="user sub to validate against"
    )
