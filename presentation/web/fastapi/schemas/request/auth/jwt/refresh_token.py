from pydantic import BaseModel


class RefreshJwtTokenRequestSchema(BaseModel):
    refresh_token: str
