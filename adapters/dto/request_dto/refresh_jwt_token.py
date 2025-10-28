from pydantic import BaseModel


class RefreshJwtTokenDto(BaseModel):
    refresh_token: str
