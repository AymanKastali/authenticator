from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Self


@dataclass(frozen=True, slots=True, kw_only=True)
class DateTimeVo:
    """
    Immutable Value Object representing a point in time.
    All validations and normalization are done in the factory.
    """

    value: datetime

    # ----------------- Domain Behavior / State Checks -----------------
    def is_future(self, reference: datetime | None = None) -> bool:
        now = reference or datetime.now(tz=self.value.tzinfo)
        return self.value > now

    def is_past(self, reference: datetime | None = None) -> bool:
        now = reference or datetime.now(tz=self.value.tzinfo)
        return self.value < now

    def is_before(self, other: Self) -> bool:
        return self.value < other.value

    def is_after(self, other: Self) -> bool:
        return self.value > other.value

    # ----------------- Comparison & String -----------------
    def __eq__(self, other: Self) -> bool:
        return self.value == other.value

    def __lt__(self, other: Self) -> bool:
        return self.value < other.value

    def __str__(self) -> str:
        return self.value.isoformat()
