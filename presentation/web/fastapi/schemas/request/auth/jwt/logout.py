from pydantic import BaseModel


class LogoutJwtRequestSchema(BaseModel):
    token: str
