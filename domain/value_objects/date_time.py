from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Self


@dataclass(frozen=True, slots=True, kw_only=True)
class DateTimeVo:
    value: datetime = field()

    def __post_init__(self) -> None:
        # Ensure datetime is timezone-aware
        aware_dt = self._make_aware(self.value)
        object.__setattr__(self, "value", aware_dt)
        # No automatic validation — validations are explicit now

    # ----------------- Validation Methods -----------------
    def validate_not_in_future(self) -> None:
        """Raise if this datetime is in the future."""
        if self.is_future():
            raise ValueError("Timestamp cannot be in the future")

    def validate_in_future(self) -> None:
        """Raise if this datetime is not in the future."""
        if not self.is_future():
            raise ValueError("Timestamp must be in the future")

    def validate_in_past(self) -> None:
        """Raise if this datetime is not in the past."""
        if not self.is_past():
            raise ValueError("Timestamp must be in the past")

    # ----------------- Helper Methods -----------------
    def _make_aware(self, dt: datetime) -> datetime:
        """Convert naive datetime to UTC-aware datetime."""
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)

    # ----------------- Factory Methods -----------------
    @classmethod
    def now(cls) -> Self:
        return cls(value=datetime.now(timezone.utc))

    @classmethod
    def from_iso(cls, iso_str: str) -> Self:
        return cls(value=datetime.fromisoformat(iso_str))

    @classmethod
    def from_timestamp(cls, ts: float) -> Self:
        return cls(value=datetime.fromtimestamp(ts, tz=timezone.utc))

    def to_iso(self) -> str:
        return self.value.isoformat()

    def to_timestamp(self) -> float:
        return self.value.timestamp()

    # ----------------- Time Arithmetic -----------------
    def add(self, **kwargs) -> Self:
        return type(self)(value=self.value + timedelta(**kwargs))

    def subtract(self, **kwargs) -> Self:
        return type(self)(value=self.value - timedelta(**kwargs))

    def subtract_seconds(self, seconds: float) -> Self:
        return self.subtract(seconds=seconds)

    def expires_after(self, seconds: float) -> Self:
        return self.add(seconds=seconds)

    # ----------------- State Checks -----------------
    def is_future(self) -> bool:
        return self.value > datetime.now(timezone.utc)

    def is_past(self) -> bool:
        return self.value < datetime.now(timezone.utc)

    def is_before(self, other: DateTimeVo) -> bool:
        return self.value < other.value

    def is_after(self, other: DateTimeVo) -> bool:
        return self.value > other.value

    # ----------------- Comparison Operators -----------------
    def __eq__(self, other: DateTimeVo) -> bool:
        return self.value == other.value

    def __lt__(self, other: DateTimeVo) -> bool:
        return self.value < other.value

    def __str__(self) -> str:
        return self.value.isoformat()
