from pydantic import BaseModel, ConfigDict


class AuthenticatedUserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: str
    email: str
    status: str
    created_at: str
    updated_at: str
    deleted_at: str | None = None
    roles: list[str] = []
