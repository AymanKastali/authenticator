from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True, kw_only=True)
class UUIDVo:
    value: UUID

    @classmethod
    def new(cls) -> Self:
        return cls(value=uuid4())

    @classmethod
    def from_string(cls, value: str) -> Self:
        return cls(value=UUID(value))

    @classmethod
    def from_uuid(cls, value: UUID) -> Self:
        return cls(value=value)

    def to_string(self) -> str:
        return str(self.value)

    def to_uuid(self) -> UUID:
        return self.value
