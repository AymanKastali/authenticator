from datetime import datetime, timedelta, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_now_time_stamp() -> float:
    return datetime.now(timezone.utc).timestamp()


def expires_after(
    *, days: float = 0, minutes: float = 0, seconds: float = 0
) -> datetime:
    if days < 0 or minutes < 0 or seconds < 0:
        raise ValueError("All time parameters must be non-negative.")

    delta = timedelta(days=days, minutes=minutes, seconds=seconds)
    return utc_now() + delta


def make_aware(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
