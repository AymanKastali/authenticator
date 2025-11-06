from pydantic import BaseModel, ConfigDict


class PublicUserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: str
    email: str
    status: str = False
