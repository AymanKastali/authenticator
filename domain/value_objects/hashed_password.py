from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class HashedPasswordVo:
    value: str

    @classmethod
    def from_string(cls, hashed_value: str) -> Self:
        """
        Create a HashedPasswordVo instance from an existing hashed string.
        """
        return cls(value=hashed_value)

    def to_string(self) -> str:
        """Return the hashed password as a raw string."""
        return self.value
