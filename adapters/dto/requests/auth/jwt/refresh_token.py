from pydantic import BaseModel


class RefreshJwtTokenInDto(BaseModel):
    refresh_token: str
