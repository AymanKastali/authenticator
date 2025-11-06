from pydantic import BaseModel, ConfigDict


class SessionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: str
    user_id: str
