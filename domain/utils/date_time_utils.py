from datetime import datetime, timedelta, timezone


def utc_now() -> "datetime":
    return datetime.now(timezone.utc)


def expires_after_minutes(ttl_minutes: int | float) -> datetime:
    if ttl_minutes < 0:
        raise ValueError("TTL in minutes must be non-negative.")
    return utc_now() + timedelta(minutes=ttl_minutes)


def expires_after_days(ttl_days: int | float) -> datetime:
    if ttl_days < 0:
        raise ValueError("TTL in days must be non-negative.")
    return utc_now() + timedelta(days=ttl_days)


def make_aware(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
