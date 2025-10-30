from pydantic import BaseModel


class LogoutJwtInDto(BaseModel):
    token: str
