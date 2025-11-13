from __future__ import annotations

from enum import StrEnum
from typing import Self, Type, TypeVar

T = TypeVar("T", bound="StringEnumVo")


class StringEnumVo(StrEnum):
    """
    Base class for string-based Value Object enums.

    Provides:
      - `keys()` to list all enum members
      - `values()` to list all string values
      - `from_string()` for case-insensitive conversion
    """

    @classmethod
    def keys(cls: Type[T]) -> list[T]:
        """Return all enum members."""
        return list(cls)

    @classmethod
    def values(cls) -> list[str]:
        """Return all string values of the enum."""
        return [member.value for member in cls]

    @classmethod
    def from_string(cls: Type[T], value: str) -> T:
        """
        Case-insensitive conversion from string to enum member.

        Raises:
            ValueError: If the value is not a valid enum member.
        """
        normalized = value.strip().upper()
        try:
            # Use a dictionary lookup for O(1) performance
            return cls._lookup()[normalized]
        except KeyError as e:
            raise ValueError(
                f"Invalid {cls.__name__} value: '{value}'. Allowed values: {cls.values()}"
            ) from e

    @classmethod
    def _lookup(cls) -> dict[str, Self]:
        """Internal helper to create a mapping of normalized values to enum members."""
        return {member.value.upper(): member for member in cls}

    def __str__(self) -> str:
        return self.value
