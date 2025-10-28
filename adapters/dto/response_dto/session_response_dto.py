from pydantic import BaseModel, ConfigDict


class SessionOutDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: str
    user_id: str
