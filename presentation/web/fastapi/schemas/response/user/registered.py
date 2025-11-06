from pydantic import BaseModel, ConfigDict


class RegisteredUserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: str
    email: str
    status: str
