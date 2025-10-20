from pydantic import BaseModel, ConfigDict


class JwtResponseResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
