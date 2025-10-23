from pydantic import BaseModel, ConfigDict


class SessionResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: str
