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


class PublicUserResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: str
    email: str
    active: bool
    verified: bool = False


class UserResponseModel(PublicUserResponseModel):
    model_config = ConfigDict(from_attributes=True)

    is_active: bool
    created_at: str
    updated_at: str
    hashed_password: str | None = None
    deleted_at: str | None = None


class AuthenticatedUserResponseModel(BaseModel):
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

    # @classmethod
    # def from_dto(cls, dto: UserDTO) -> "AuthenticatedUserResponseModel":
    #     return cls(
    #         uid=dto.uid,
    #         email=dto.email,
    #         is_active=dto.is_active,
    #         active=dto.active,
    #         verified=dto.verified,
    #         created_at=dto.created_at,
    #         updated_at=dto.updated_at,
    #         hashed_password=dto.hashed_password,
    #         deleted_at=dto.deleted_at,
    #     )
