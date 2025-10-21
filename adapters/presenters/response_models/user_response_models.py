from pydantic import BaseModel, ConfigDict


class RegisteredUserResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: str
    email: str
    is_active: bool
    active: bool
    verified: bool
    created_at: str
    updated_at: str
    hashed_password: str | None = None
    deleted_at: str | None = None
