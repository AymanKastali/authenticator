from pydantic import BaseModel, ConfigDict


class RegisteredUserOutDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: str
    email: str
    status: str
