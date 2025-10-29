from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReadMeOutDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: str
    email: str
    active: bool
    verified: bool
    created_at: str
    updated_at: str
    deleted_at: str | None = None

    def as_uuid(self) -> UUID:
        return UUID(self.uid)
