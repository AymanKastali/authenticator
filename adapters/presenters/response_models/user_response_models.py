from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RegisteredUserResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: str
    email: str
    active: bool
    verified: bool


class PublicUserResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: str
    email: str
    active: bool
    verified: bool = False


class UserResponseModel(PublicUserResponseModel):
    model_config = ConfigDict(from_attributes=True)

    active: bool
    created_at: str
    updated_at: str
    deleted_at: str | None = None


class AuthenticatedUserResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: str
    email: str
    active: bool
    verified: bool
    created_at: str
    updated_at: str
    deleted_at: str | None = None

    def uid_as_uuid(self) -> UUID:
        return UUID(self.uid)
