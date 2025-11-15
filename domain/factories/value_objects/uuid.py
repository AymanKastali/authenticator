import uuid
from uuid import UUID

from domain.value_objects.uuid_id import UUIDVo


class UUIDVoFactory:
    @classmethod
    def new(cls) -> UUIDVo:
        """Create a new random UUIDVo"""
        return UUIDVo(_value=uuid.uuid4())

    @classmethod
    def from_string(cls, value: str) -> UUIDVo:
        """Create a UUIDVo from a string"""
        return UUIDVo(_value=UUID(value))

    @classmethod
    def from_uuid(cls, value: UUID) -> UUIDVo:
        """Create a UUIDVo from an existing UUID object"""
        return UUIDVo(_value=value)
