from pydantic import BaseModel, ConfigDict


class PublicUserOutDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: str
    email: str
    active: bool
    verified: bool = False
