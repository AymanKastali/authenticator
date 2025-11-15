from datetime import datetime, timedelta, timezone

from domain.value_objects.date_time import DateTimeVo


class DateTimeVoFactory:
    """Factory responsible for creating valid DateTimeVo instances."""

    @classmethod
    def now(cls) -> DateTimeVo:
        dt = datetime.now(timezone.utc)
        return cls._create(dt)

    @classmethod
    def from_iso(cls, iso_str: str) -> DateTimeVo:
        dt = datetime.fromisoformat(iso_str)
        return cls._create(dt)

    @classmethod
    def from_timestamp(cls, ts: float) -> DateTimeVo:
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return cls._create(dt)

    @classmethod
    def from_datetime(cls, dt: datetime) -> DateTimeVo:
        return cls._create(dt)

    @classmethod
    def plus_seconds(cls, dt_vo: DateTimeVo, seconds: float) -> DateTimeVo:
        return cls._create(dt_vo.value + timedelta(seconds=seconds))

    @classmethod
    def minus_seconds(cls, dt_vo: DateTimeVo, seconds: float) -> DateTimeVo:
        return cls._create(dt_vo.value - timedelta(seconds=seconds))

    @classmethod
    def expires_after(cls, dt_vo: DateTimeVo, seconds: float) -> DateTimeVo:
        return cls.plus_seconds(dt_vo, seconds)

    # ----------------- Internal Creation with Normalization & Validation -----------------
    @classmethod
    def _create(cls, dt: datetime) -> DateTimeVo:
        """Normalize and enforce invariants before returning VO."""
        dt_aware = cls._ensure_utc(dt)
        cls._enforce_not_naive(dt_aware)
        return DateTimeVo(value=dt_aware)

    @staticmethod
    def _ensure_utc(dt: datetime) -> datetime:
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)

    @staticmethod
    def _enforce_not_naive(dt: datetime) -> None:
        if dt.tzinfo is None:
            raise ValueError("Datetime must be timezone-aware")
