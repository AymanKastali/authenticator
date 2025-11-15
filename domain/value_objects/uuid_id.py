from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class UUIDVo:
    _value: UUID

    @property
    def value(self) -> str:
        return str(self._value)
